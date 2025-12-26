"""
Document Type Registry
Manages document type definitions and prompts
"""

from typing import Dict, Optional
from pathlib import Path


class DocumentTypeRegistry:
    """Registry for document types and their configurations"""
    
    def __init__(self):
        self._document_types: Dict[str, Dict] = {}
        self._prompts: Dict[str, str] = {}
        self._load_document_types()
        self._load_prompts()
    
    def _load_document_types(self):
        """Load document type definitions"""
        self._document_types = {
            "Index 2": {
                "display_name": "Index 2",
                "fields": [
                    "Document_number/ दस्त क्रमांक",
                    "Seller/देनारा",
                    "Buyer/घेणारा",
                    "property_address_with_gat_numbers/ पत्ता"
                ],
                "service": "PT5"
            },
            "NOC": {
                "display_name": "NOC",
                "fields": ["Name", "Flat No", "Address"],
                "service": "PT5"
            },
            "No Dues": {
                "display_name": "No Dues",
                "fields": ["Name", "Address", "Amount"],
                "service": "PT5"
            }
        }
    
    def _load_prompts(self):
        """Load prompts from individual markdown files per document type"""
        prompts_dir = Path(__file__).parent.parent / "prompts"
        
        # Map document types to their corresponding prompt file names
        doc_type_to_file = {
            "NOC": "NOC.md",
            "Index 2": "Index 2.md",
            "No Dues": "No Dues.md"
        }
        
        # Try current project prompts folder first
        if not prompts_dir.exists():
            # Fallback: use prompts from testing LLM's folder
            prompts_dir = Path("/home/stark/testing LLM's")
        
        # Load each prompt file
        for doc_type, filename in doc_type_to_file.items():
            prompt_file = prompts_dir / filename
            
            if prompt_file.exists():
                try:
                    content = prompt_file.read_text(encoding='utf-8')
                    self._prompts[doc_type] = content.strip()
                except Exception as e:
                    print(f"Warning: Failed to load prompt for {doc_type} from {prompt_file}: {e}")
            else:
                print(f"Warning: Prompt file not found for {doc_type}: {prompt_file}")
        
        # If no prompts were loaded, use default prompts
        if not self._prompts:
            self._load_default_prompts()
    
    def _load_default_prompts(self):
        """Load default prompts if files not found"""
        # Default prompts would be loaded here if needed
        # Currently, prompts are loaded from individual .md files per document type
        pass
    
    def get_document_type(self, doc_type: str) -> Optional[Dict]:
        """Get document type configuration"""
        return self._document_types.get(doc_type)
    
    def get_prompt(self, doc_type: str) -> Optional[str]:
        """Get prompt for a document type"""
        return self._prompts.get(doc_type)
    
    def list_document_types(self) -> list:
        """List all registered document types"""
        return list(self._document_types.keys())
    
    def is_valid_document_type(self, doc_type: str) -> bool:
        """Check if document type is valid"""
        return doc_type in self._document_types
    
    def register_document_type(self, doc_type: str, config: Dict, prompt: str = ""):
        """
        Register a new document type (for future extensibility)
        
        Args:
            doc_type: Document type name
            config: Configuration dictionary
            prompt: Prompt text for this document type
        """
        self._document_types[doc_type] = config
        if prompt:
            self._prompts[doc_type] = prompt


# Global registry instance
_registry: Optional[DocumentTypeRegistry] = None


def get_document_registry() -> DocumentTypeRegistry:
    """Get global document registry instance"""
    global _registry
    if _registry is None:
        _registry = DocumentTypeRegistry()
    return _registry

