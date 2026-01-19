"""
Pydantic models for API request/response
"""

from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field, HttpUrl


class DocumentInfo(BaseModel):
    """Document information from PMC"""
    download_url: str = Field(..., description="URL to download the document")
    document_type: str = Field(..., description="Type of document (Index 2, NOC, No Dues)")
    actual_data: Dict[str, Any] = Field(..., description="Actual/ground truth data for verification")


class VerificationRequest(BaseModel):
    """Request model for document verification"""
    service_name: str = Field(..., description="Service name (e.g., PT5)")
    appNo: str = Field(..., description="Unique app number")
    documents: List[DocumentInfo] = Field(..., description="List of documents to verify")

    class Config:
        json_schema_extra = {
            "example": {
                "service_name": "PT5",
                "appNo": "SJG635YS",
                "documents": [
                    {
                        "download_url": "https://pmc.gov.in/docs/doc1.pdf",
                        "document_type": "Index 2",
                        "actual_data": {
                            "Document_number/ दस्त क्रमांक": "13862/2021",
                            "Seller/देनारा": ["आर्मी वेलफेअर..."],
                            "Buyer/घेणारा": ["प्रशांतचंद्र..."],
                            "property_address_with_gat_numbers/ पत्ता": "..."
                        }
                    }
                ]
            }
        }


class FieldAccuracy(BaseModel):
    """Field-level accuracy information"""
    accuracy: float = Field(..., ge=0.0, le=1.0, description="Accuracy score (0-1)")
    actual: str = Field(..., description="Actual value")
    predicted: str = Field(..., description="Predicted value from LLM")
    method: str = Field(..., description="Method used (exact_match, fuzzy, hybrid)")
    details: Optional[str] = Field(None, description="Additional details")


class DocumentResult(BaseModel):
    """Result for a single document"""
    document_type: str = Field(..., description="Document type")
    document_url: str = Field(..., description="Original document URL")
    success: bool = Field(..., description="Whether processing was successful")
    accuracy: float = Field(..., ge=0.0, le=1.0, description="Overall accuracy score")
    fields_accuracy: Dict[str, FieldAccuracy] = Field(..., description="Field-level accuracy")
    extracted_fields: Dict[str, str] = Field(default_factory=dict, description="Extracted fields from LLM")
    error: Optional[str] = Field(None, description="Error message if processing failed")
    llm_output: Optional[str] = Field(None, description="Raw LLM output")
    processing_time: Optional[float] = Field(None, description="Processing time in seconds")


class VerificationResponse(BaseModel):
    """Response model for document verification"""
    success: bool = Field(..., description="Whether verification was successful")
    service_name: str = Field(..., description="Service name")
    total_documents: int = Field(..., description="Total number of documents processed")
    successful: int = Field(..., description="Number of successfully processed documents")
    failed: int = Field(..., description="Number of failed documents")
    average_accuracy: float = Field(..., ge=0.0, le=1.0, description="Average accuracy across all documents")
    results: List[DocumentResult] = Field(..., description="Results for each document")


class HealthResponse(BaseModel):
    """Health check response"""
    status: str = Field(..., description="Service status")
    version: str = Field(..., description="API version")
    timestamp: str = Field(..., description="Current timestamp")

