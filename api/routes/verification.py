"""
Verification API routes
Handles document verification requests from PMC
"""
import os
import time
import tempfile
import shutil
import uuid
import asyncio
from pathlib import Path
from typing import List, Dict, Any

from fastapi import APIRouter, HTTPException, BackgroundTasks, Request
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
from services.webhook import post_data_via_webhook
from utils.file_handler import download_file, get_file_extension
from api.routes.tasks import process_docs  # Import the Celery task

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
        task_id = str(uuid.uuid4())
        
        # Queue the task with Celery (convert Path to string for serialization)
        task = process_docs.delay({
            "documents": documents_data,
            "service_name": request.service_name,
            "temp_dir": str(temp_dir),  # Convert Path to string for JSON serialization
            "task_id": task_id
        })

        return {
            "success": True,
            "service_name": request.service_name,
            "appNo": request.appNo,
            "task_id": task_id
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


@router.post("/webhook")
async def get_webhook_data(request: Request):
    """
    Get webhook data
    
    Returns:
        Webhook data
    """
    print(await request.json())
    return JSONResponse(content={"message": "Webhook received"}, status_code=200)
