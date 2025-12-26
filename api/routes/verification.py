"""
Verification API routes
Handles document verification requests from PMC
"""
import os
import time
import tempfile
import shutil
import asyncio
from pathlib import Path
from typing import List, Dict, Any

from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse

from api.models.schemas import (
    VerificationRequest,
    VerificationResponse,
    DocumentResult,
    FieldAccuracy
)
from core import DocumentProcessor, AccuracyCalculator
from core.service_registry import get_service_registry
from config import get_settings, get_document_registry
from services.middleware import require_bearer_auth
from services.webhook import post_data_via_webhook
from utils.file_handler import download_file, get_file_extension
from core.celery import celery_app as _celery

router = APIRouter(prefix="/api/v1", tags=["verification"])


async def process_single_document(
    doc_info: dict,
    service_name: str,
    temp_dir: Path
) -> DocumentResult:
    """
    Process a single document
    
    Args:
        doc_info: Document information from request
        service_name: Service name
        temp_dir: Temporary directory for downloaded files
        
    Returns:
        DocumentResult with accuracy information
    """
    settings = get_settings()
    doc_registry = get_document_registry()
    service_registry = get_service_registry()
    
    document_type = doc_info["document_type"]
    download_url = doc_info["download_url"]
    actual_data = doc_info["actual_data"]
    
    # Validate service and document type
    if not service_registry.is_valid_service(service_name):
        raise HTTPException(
            status_code=400,
            detail=f"Invalid service: {service_name}"
        )
    
    if not service_registry.is_valid_document_type_for_service(service_name, document_type):
        raise HTTPException(
            status_code=400,
            detail=f"Document type '{document_type}' is not valid for service '{service_name}'"
        )
    
    if not doc_registry.is_valid_document_type(document_type):
        raise HTTPException(
            status_code=400,
            detail=f"Invalid document type: {document_type}"
        )
    
    # Get prompt for document type
    prompt = doc_registry.get_prompt(document_type)
    if not prompt:
        raise HTTPException(
            status_code=500,
            detail=f"No prompt found for document type: {document_type}"
        )
    
    # Download document
    # Get extension from URL if available, but don't force a default
    # The file_handler will detect the actual type after download
    file_ext = get_file_extension(str(download_url))
    if not file_ext:
        file_ext = ""  # Let file_handler detect the type
    
    temp_file = temp_dir / f"doc_{int(time.time())}{file_ext}"
    
    try:
        # download_file may return a different path if it renames the file
        actual_file_path = await download_file(str(download_url), temp_file)
    except Exception as e:
        return DocumentResult(
            document_type=document_type,
            document_url=str(download_url),
            success=False,
            accuracy=0.0,
            fields_accuracy={},
            error=f"Failed to download document: {str(e)}"
        )
    
    # Process document with LLM
    processor = None
    try:
        processor = DocumentProcessor(
            model_name=settings.default_model,
            document_type=document_type,
            settings=settings
        )
        
        result = processor.process_document(
            document_path=actual_file_path,
            prompt=prompt
        )
        
        if not result.get("success", False):
            return DocumentResult(
                document_type=document_type,
                document_url=str(download_url),
                success=False,
                accuracy=0.0,
                fields_accuracy={},
                error=result.get("error", "Unknown error"),
                llm_output=result.get("content", "")
            )
        
        llm_output = result.get("content", "")
        
        # Calculate accuracy
        calculator = AccuracyCalculator(settings=settings)
        accuracy_result = calculator.calculate_accuracy(
            llm_output=llm_output,
            actual_data=actual_data,
            document_id=actual_data.get("Document id")
        )
        
        # Convert fields_accuracy to FieldAccuracy objects
        fields_accuracy = {}
        for field_name, field_data in accuracy_result.get("fields_accuracy", {}).items():
            fields_accuracy[field_name] = FieldAccuracy(
                accuracy=field_data["accuracy"],
                actual=field_data["actual"],
                predicted=field_data["predicted"],
                method=field_data["method"],
                details=field_data.get("details")
            )
        
        return DocumentResult(
            document_type=document_type,
            document_url=str(download_url),
            success=True,
            accuracy=accuracy_result["accuracy"],
            fields_accuracy=fields_accuracy,
            extracted_fields=accuracy_result.get("extracted_fields", {}),
            llm_output=llm_output
        )
        
    except Exception as e:
        return DocumentResult(
            document_type=document_type,
            document_url=str(download_url),
            success=False,
            accuracy=0.0,
            fields_accuracy={},
            error=f"Processing error: {str(e)}"
        )
    finally:
        if processor:
            processor.close()
        # Clean up temp file (use actual_file_path in case it was renamed)
        try:
            if actual_file_path.exists():
                actual_file_path.unlink()
        except Exception:
            pass  # Ignore cleanup errors


@router.post("/verify")
@require_bearer_auth
async def verify_documents(
    request: VerificationRequest,
    background_tasks: BackgroundTasks
):
    """
    Verify documents
    
    This endpoint:
    1. Downloads documents from provided URLs
    2. Processes them through our AI System
    3. Calculates accuracy by comparing output with actual data
    4. Returns field-level accuracy for each document
    
    Args:
        request: Verification request with documents and actual data
        background_tasks:  background tasks (for cleanup)
        
    Returns:
        VerificationResponse with accuracy results for each document
    """
    try:

        # Create temporary directory for downloads
        temp_dir = Path(tempfile.mkdtemp())
        # Use shutil.rmtree to remove directory and all contents
        background_tasks.add_task(lambda: shutil.rmtree(temp_dir, ignore_errors=True) if temp_dir.exists() else None)
        
        # Convert Pydantic models to dicts for Celery serialization
        documents_data = [doc.dict() for doc in request.documents]
        
        # Queue the task with Celery (convert Path to string for serialization)
        task = process_docs.delay({
            "documents": documents_data,
            "service_name": request.service_name,
            "temp_dir": str(temp_dir),  # Convert Path to string for JSON serialization
        })

        return {
            "success": True,
            "service_name": request.service_name,
            "appNo": request.appNo
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )
        

@router.get("/health", response_model=dict)
async def health_check() -> dict:
    """
    Health check endpoint
    
    Returns:
        Health status information
    """
    from datetime import datetime
    settings = get_settings()
    
    return {
        "status": "healthy",
        "version": settings.api_version,
        "timestamp": datetime.now().isoformat()
    }

def process_single_document_sync(
    doc_info: dict,
    service_name: str,
    temp_dir: Path
) -> Dict[str, Any]:
    """
    Synchronous wrapper for process_single_document
    Runs the async function in an event loop
    
    Args:
        doc_info: Document information from request (as dict)
        service_name: Service name
        temp_dir: Temporary directory for downloaded files (as Path or str)
        
    Returns:
        Dictionary representation of DocumentResult
    """
    # Convert temp_dir to Path if it's a string
    if isinstance(temp_dir, str):
        temp_dir = Path(temp_dir)
    
    # Run the async function in a new event loop
    # asyncio.run() creates a new event loop, runs the coroutine, and closes the loop
    # This is safe to use in Celery tasks which run in separate processes
    result = asyncio.run(process_single_document(doc_info, service_name, temp_dir))
    
    # Convert DocumentResult Pydantic model to dict for JSON serialization
    return result.dict() if hasattr(result, 'dict') else result


@_celery.task
def process_docs(data: Dict):
    """
    Celery task to process documents asynchronously
    
    Args:
        data: Dictionary containing:
            - documents: List of document info dicts
            - service_name: Service name string
            - temp_dir: Temporary directory path as string
            
    Returns:
        Dictionary with processing results
    """
    try:
        # Extract data from dictionary (Celery serializes everything as dict)
        documents = data.get("documents", [])
        service_name = data.get("service_name", "")
        temp_dir_str = data.get("temp_dir", "")
        
        # Convert temp_dir string back to Path
        temp_dir = Path(temp_dir_str) if temp_dir_str else Path(tempfile.mkdtemp())
        
        # Process all documents
        results: List[Dict[str, Any]] = []
        
        for doc_info in documents:
            # doc_info is already a dict from Celery serialization
            # If it's a Pydantic model that was serialized, it's now a dict
            if not isinstance(doc_info, dict):
                # Convert to dict if it's still a model
                doc_info = doc_info.dict() if hasattr(doc_info, 'dict') else dict(doc_info)
            
            try:
                result_dict = process_single_document_sync(
                    doc_info=doc_info,
                    service_name=service_name,
                    temp_dir=temp_dir
                )
                results.append(result_dict)
            except Exception as e:
                # Handle individual document errors gracefully
                error_result = {
                    "document_type": doc_info.get("document_type", "Unknown"),
                    "document_url": doc_info.get("download_url", ""),
                    "success": False,
                    "accuracy": 0.0,
                    "fields_accuracy": {},
                    "error": f"Processing error: {str(e)}"
                }
                results.append(error_result)
        
        # Calculate summary statistics
        successful = sum(1 for r in results if r.get("success", False))
        failed = len(results) - successful
        avg_accuracy = (
            sum(r.get("accuracy", 0.0) for r in results if r.get("success", False)) / successful
            if successful > 0 else 0.0
        )
        
        # Clean up temporary directory (Celery runs in separate process, so cleanup here)
        try:
            if temp_dir.exists():
                shutil.rmtree(temp_dir, ignore_errors=True)
        except Exception:
            pass  # Ignore cleanup errors
        
        response = {}
        data = {
            "success": True,
            "service_name": service_name,
            "total_documents": len(results),
            "successful": successful,
            "failed": failed,
            "average_accuracy": avg_accuracy,
            "results": results,
        }
        
        if os.getenv("WEBHOOK_ENABLE"):
            if webhook_url := os.getenv("WEBHOOK_URL"):
                response = post_data_via_webhook(
                    url=webhook_url,
                    data=data,
                    timeout=350,
                    headers={
                        "Authorization": f"Bearer {os.getenv('WEBHOOK_TOKEN')}",
                        "Accept": "application/json",
                    }
                )
            else:
                print("Webhook url is missing, Please add it into the .env")

        print("Response : ", response)

    except Exception as e:
        # Clean up temporary directory even on error
        try:
            if 'temp_dir' in locals() and temp_dir.exists():
                shutil.rmtree(temp_dir, ignore_errors=True)
        except Exception:
            pass
        
        # Return error result instead of raising HTTPException (Celery tasks shouldn't raise HTTPException)
        return {
            "success": False,
            "error": f"Internal server error: {str(e)}",
            "total_documents": 0,
            "successful": 0,
            "failed": 0,
            "average_accuracy": 0.0,
            "results": [],
        }


