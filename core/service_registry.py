"""
Service Registry
Manages services and their associated document types
Enables easy extensibility for future services
"""

from typing import Dict, List, Optional
from config import DocumentTypeRegistry, get_document_registry


class ServiceRegistry:
    """Registry for services and their document types"""
    
    def __init__(self):
        self._services: Dict[str, Dict] = {}
        self._document_registry = get_document_registry()
        self._load_services()
    
    def _load_services(self):
        """Load service definitions"""
        # PT5 Service
        self._services["PT5"] = {
            "name": "PT5",
            "display_name": "PT5 Service",
            "document_types": ["Index 2", "NOC", "No Dues"],
            "description": "Property Tax Service - Document Verification"
        }
    
    def get_service(self, service_name: str) -> Optional[Dict]:
        """Get service configuration"""
        return self._services.get(service_name.upper())
    
    def list_services(self) -> List[str]:
        """List all registered services"""
        return list(self._services.keys())
    
    def get_document_types_for_service(self, service_name: str) -> List[str]:
        """Get document types for a service"""
        service = self.get_service(service_name)
        if service:
            return service.get("document_types", [])
        return []
    
    def is_valid_service(self, service_name: str) -> bool:
        """Check if service is valid"""
        return service_name.upper() in self._services
    
    def is_valid_document_type_for_service(self, service_name: str, document_type: str) -> bool:
        """Check if document type is valid for a service"""
        doc_types = self.get_document_types_for_service(service_name)
        return document_type in doc_types
    
    def register_service(
        self, 
        service_name: str, 
        document_types: List[str], 
        display_name: Optional[str] = None,
        description: Optional[str] = None
    ):
        """
        Register a new service (for future extensibility)
        
        Args:
            service_name: Service identifier
            document_types: List of document type names
            display_name: Optional display name
            description: Optional description
        """
        self._services[service_name.upper()] = {
            "name": service_name.upper(),
            "display_name": display_name or service_name,
            "document_types": document_types,
            "description": description or ""
        }


# Global registry instance
_registry: Optional[ServiceRegistry] = None


def get_service_registry() -> ServiceRegistry:
    """Get global service registry instance"""
    global _registry
    if _registry is None:
        _registry = ServiceRegistry()
    return _registry

