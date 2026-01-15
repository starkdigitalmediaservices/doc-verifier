"""
Settings management from environment variables
Handles preprocessing mode configuration per document type
"""

import os
from typing import Dict
from functools import lru_cache

try:
    from pydantic_settings import BaseSettings
    from pydantic import ConfigDict
    PYDANTIC_V2 = True
except ImportError:
    # Fallback for older pydantic versions
    from pydantic import BaseSettings
    PYDANTIC_V2 = False


class Settings(BaseSettings):
    """Application settings from environment variables"""
    
    # GitHub Models API
    github_token: str
    
    # Model Configuration
    default_model: str = "Llama 4 Maverick 17B 128E Instruct FP8"
    default_temperature: float = 0.7
    default_max_tokens: int = 2000
    api_timeout_seconds: int = 120
    
    # Preprocessing Mode (per document type)
    # 0 = No preprocessing, 1 = Token optimization (resize/compress), 2 = Quality enhancement
    # These can be set in .env as: PREPROCESSING_INDEX_2=0
    preprocessing_index_2: int = 0
    preprocessing_noc: int = 1
    preprocessing_no_dues: int = 1
    
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

    # Pydantic v2 syntax (works with pydantic_settings)
    if ConfigDict is not None:
        model_config = ConfigDict(
            env_file=".env",
            case_sensitive=False,
            extra="ignore"  # Ignore extra environment variables (e.g., preprocessing config vars)
        )
    else:
        # Pydantic v1 syntax (fallback)
        class Config:
            env_file = ".env"
            case_sensitive = False
            extra = "ignore"  # Ignore extra environment variables (e.g., preprocessing config vars)

    def get_preprocessing_mode(self, document_type: str) -> int:
        """
        Get preprocessing mode for a specific document type
        
        Args:
            document_type: Document type name (e.g., "Index 2", "NOC", "No Dues")
            
        Returns:
            Preprocessing mode: 0 (none), 1 (token optimization), or 2 (quality enhancement)
        """
        # Normalize document type name for env variable lookup
        doc_type_normalized = document_type.upper().replace(" ", "_").replace("-", "_")
        
        # Check for specific env variable
        env_var = f"PREPROCESSING_{doc_type_normalized}"
        value = os.getenv(env_var)
        
        if value is not None:
            try:
                mode = int(value)
                # Validate mode is 0, 1, or 2
                if mode in (0, 1, 2):
                    return mode
            except ValueError:
                pass  # Fall back to defaults
        
        # Fallback to default based on document type
        preprocessing_map = {
            "INDEX_2": self.preprocessing_index_2,
            "NOC": self.preprocessing_noc,
            "NO_DUES": self.preprocessing_no_dues,
        }
        
        return preprocessing_map.get(doc_type_normalized, 1)  # Default to token optimization
    
    def get_preprocessing_config(self) -> Dict[str, int]:
        """
        Get all preprocessing mode settings as a dictionary
        
        Returns:
            Dictionary mapping document types to preprocessing modes (0, 1, or 2)
        """
        return {
            "Index 2": self.get_preprocessing_mode("Index 2"),
            "NOC": self.get_preprocessing_mode("NOC"),
            "No Dues": self.get_preprocessing_mode("No Dues"),
        }


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()

