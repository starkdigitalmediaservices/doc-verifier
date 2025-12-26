"""
Settings management from environment variables
Handles token optimization toggles per document type
"""

import os
from typing import Dict
from functools import lru_cache

try:
    from pydantic_settings import BaseSettings
except ImportError:
    # Fallback for older pydantic versions
    from pydantic import BaseSettings


class Settings(BaseSettings):
    """Application settings from environment variables"""
    
    # GitHub Models API
    github_token: str
    
    # Model Configuration
    default_model: str = "Llama 4 Maverick 17B 128E Instruct FP8"
    default_temperature: float = 0.7
    default_max_tokens: int = 2000
    api_timeout_seconds: int = 120
    
    # Token Optimization Toggle (per document type)
    # These can be set in .env as: TOKEN_OPTIMIZATION_INDEX_2=false
    token_optimization_index_2: bool = False
    token_optimization_noc: bool = True
    token_optimization_no_dues: bool = True
    
    # Image Optimization Settings (when enabled)
    max_image_width: int = 1536
    max_image_height: int = 1536
    jpeg_quality: int = 85
    enable_auto_crop: bool = False
    enable_grayscale: bool = False
    
    # Embedding Model
    embedding_model_name: str = "intfloat/multilingual-e5-base"
    embedding_dimension: int = 768
    
    # API Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 5002
    api_title: str = "Document Verification API"
    api_version: str = "1.0.0"
    
    # Logging
    log_level: str = "INFO"
    
    # Security Settings
    api_token: str = ""  # API token for endpoint protection (set via API_TOKEN env var)
    swagger_password: str = ""  # Password for Swagger UI protection (set via SWAGGER_PASSWORD env var)
    
    celery_broker_url: str = "redis://localhost:6379/0"
    celery_result_backend: str = "redis://localhost:6379/1"
    
    # Webhook Settings
    bearer_token: str = ""
    webhook_url: str = ""
    webhook_token: str = ""
    webhook_enable: bool = False

    class Config:
        env_file = ".env"
        case_sensitive = False

    def get_token_optimization(self, document_type: str) -> bool:
        """
        Get token optimization setting for a specific document type
        
        Args:
            document_type: Document type name (e.g., "Index 2", "NOC", "No Dues")
            
        Returns:
            True if optimization should be enabled, False otherwise
        """
        # Normalize document type name for env variable lookup
        doc_type_normalized = document_type.upper().replace(" ", "_").replace("-", "_")
        
        # Check for specific env variable
        env_var = f"TOKEN_OPTIMIZATION_{doc_type_normalized}"
        value = os.getenv(env_var)
        
        if value is not None:
            return value.lower() in ("true", "1", "yes", "on")
        
        # Fallback to default based on document type
        optimization_map = {
            "INDEX_2": self.token_optimization_index_2,
            "NOC": self.token_optimization_noc,
            "NO_DUES": self.token_optimization_no_dues,
        }
        
        return optimization_map.get(doc_type_normalized, True)
    
    def get_optimization_config(self) -> Dict[str, bool]:
        """
        Get all token optimization settings as a dictionary
        
        Returns:
            Dictionary mapping document types to optimization enabled status
        """
        return {
            "Index 2": self.get_token_optimization("Index 2"),
            "NOC": self.get_token_optimization("NOC"),
            "No Dues": self.get_token_optimization("No Dues"),
        }


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()

