"""Configuration module for Document Verification System"""

from .settings import Settings, get_settings
from .document_types import DocumentTypeRegistry, get_document_registry

__all__ = ["Settings", "get_settings", "DocumentTypeRegistry", "get_document_registry"]

