"""
Celery tasks for document verification
"""
import asyncio
import shutil
import tempfile
import time
from pathlib import Path
from typing import Dict, Any, List

from core.celery import _celery
from config import get_settings
from services.webhook import post_data_via_webhook
# Import utils first to ensure it's available when process_single_document is imported


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
    # Import here to avoid circular imports - utils is already imported at module level
    from api.routes.verification import process_single_document
    
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
        task_id = data.get("task_id", "")
        # Convert temp_dir string back to Path
        temp_dir = Path(temp_dir_str) if temp_dir_str else Path(tempfile.mkdtemp())
        
        # Process all documents
        results: List[Dict[str, Any]] = []
        total_start_time = time.time()
        
        for doc_info in documents:
            # doc_info is already a dict from Celery serialization
            # If it's a Pydantic model that was serialized, it's now a dict
            if not isinstance(doc_info, dict):
                # Convert to dict if it's still a model
                doc_info = doc_info.dict() if hasattr(doc_info, 'dict') else dict(doc_info)
            
            doc_start_time = time.time()
            try:
                result_dict = process_single_document_sync(
                    doc_info=doc_info,
                    service_name=service_name,
                    temp_dir=temp_dir
                )
                # Ensure processing_time is included (it should be from process_single_document)
                if "processing_time" not in result_dict or result_dict["processing_time"] is None:
                    result_dict["processing_time"] = time.time() - doc_start_time
                results.append(result_dict)
            except Exception as e:
                # Handle individual document errors gracefully
                doc_processing_time = time.time() - doc_start_time
                error_result = {
                    "document_type": doc_info.get("document_type", "Unknown"),
                    "document_url": doc_info.get("download_url") or doc_info.get("file_path") or "document",
                    "success": False,
                    "accuracy": 0.0,
                    "fields_accuracy": {},
                    "error": f"Processing error: {str(e)}",
                    "processing_time": doc_processing_time
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
        
        total_processing_time = time.time() - total_start_time
        
        response_data = {
            "success": True,
            "service_name": service_name,
            "total_documents": len(results),
            "successful": successful,
            "failed": failed,
            "average_accuracy": avg_accuracy,
            "results": results,
            "task_id": task_id,
            "total_processing_time": total_processing_time
        }
        
        # Post to webhook if configured
        # IMPORTANT: Webhook failures should NOT affect task result
        # Results are always returned even if webhook fails
        settings = get_settings()
        if settings.webhook_enable:
            if settings.webhook_url:
                try:
                    response = post_data_via_webhook(
                        url=settings.webhook_url,
                        data=response_data,
                        timeout=350,
                        headers={
                            "Authorization": f"Bearer {settings.webhook_token}",
                            "Accept": "application/json",
                        }
                    )
                    print("✅ Webhook Response:", response.status_code)
                except Exception as webhook_error:
                    # Log webhook error but don't fail the task
                    print(f"⚠️  Webhook delivery failed (results still available): {webhook_error}")
                    print(f"   Results: {len(results)} documents processed successfully")
                    # Add webhook error to response but keep success=True
                    response_data["webhook_error"] = str(webhook_error)
            else:
                print("⚠️  Webhook url is missing, Please add it into the .env")
        else:
            # Webhook not enabled - log results for local testing
            print(f"📋 Processing complete: {successful} successful, {failed} failed")
            print(f"   Results available (webhook disabled for local testing)")
        
        return response_data
        
    except Exception as e:
        # Clean up on error
        try:
            temp_dir_str = data.get("temp_dir", "")
            if temp_dir_str:
                temp_dir = Path(temp_dir_str)
                if temp_dir.exists():
                    shutil.rmtree(temp_dir, ignore_errors=True)
        except Exception:
            pass
        
        # Return error result instead of raising (Celery tasks shouldn't raise HTTPException)
        return {
            "success": False,
            "error": f"Internal server error: {str(e)}",
            "total_documents": 0,
            "successful": 0,
            "failed": 0,
            "average_accuracy": 0.0,
            "results": [],
            "task_id": data.get("task_id", "")
        }

