"""
Core Document Processor Module
Handles image processing and inference with LLM models
Modular version with configurable token optimization
"""

import os
import base64
import io
import threading
from pathlib import Path
from typing import Dict, Optional, List, Callable
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import (
    SystemMessage, UserMessage, ImageContentItem, 
    ImageUrl, TextContentItem
)
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
from PIL import Image

try:
    from pdf2image import convert_from_path
    PDF_SUPPORT = True
except ImportError:
    PDF_SUPPORT = False

from config import Settings, get_settings


class DocumentProcessor:
    """Processes documents using LLM models with configurable optimization"""
    
    # Model configuration
    AVAILABLE_MODELS = {
        "Llama 4 Maverick 17B 128E Instruct FP8": {
            "model_id": "meta/Llama-4-Maverick-17B-128E-Instruct-FP8",
            "endpoint": "https://models.github.ai/inference",
            "requires_image": True,
            "display_name": "Llama 4 Maverick 17B 128E Instruct FP8"
        }
    }
    
    def __init__(
        self, 
        model_name: str, 
        document_type: Optional[str] = None,
        settings: Optional[Settings] = None
    ):
        """
        Initialize the document processor
        
        Args:
            model_name: Name of the model from AVAILABLE_MODELS
            document_type: Document type to control optimization behavior
            settings: Settings instance (if None, uses get_settings())
        """
        if model_name not in self.AVAILABLE_MODELS:
            raise ValueError(f"Model '{model_name}' not found in available models")
        
        self.model_config = self.AVAILABLE_MODELS[model_name]
        self.model_name = model_name
        self.document_type = document_type
        self.settings = settings or get_settings()
        self.client = None
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize the Azure AI Inference client"""
        if not self.settings.github_token:
            raise ValueError("GITHUB_TOKEN not found in environment variables")
        
        self.client = ChatCompletionsClient(
            endpoint=self.model_config["endpoint"],
            credential=AzureKeyCredential(self.settings.github_token),
        )
    
    def _should_optimize_image(self) -> bool:
        """
        Check if image optimization should be applied based on document type and settings
        
        Returns:
            True if optimization should be enabled, False otherwise
        """
        if not self.document_type:
            return True  # Default to enabled if no document type specified
        
        return self.settings.get_token_optimization(self.document_type)
    
    def _optimize_image(self, image_path: Path) -> Image.Image:
        """
        Optimize image for token efficiency by resizing and compressing
        
        Args:
            image_path: Path to the image file
            
        Returns:
            Optimized PIL Image object
        """
        # Load image
        img = Image.open(image_path)
        
        # Convert to RGB if needed (for JPEG compatibility)
        if img.mode in ('RGBA', 'LA', 'P'):
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            background.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
            img = background
        elif img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Auto-rotate based on EXIF data
        try:
            from PIL import ImageOps
            img = ImageOps.exif_transpose(img)
        except Exception:
            pass
        
        # Auto-crop whitespace if enabled
        if self.settings.enable_auto_crop:
            try:
                gray = img.convert('L')
                bbox = gray.getbbox()
                if bbox:
                    img = img.crop(bbox)
            except Exception:
                pass
        
        # Convert to grayscale if enabled
        if self.settings.enable_grayscale:
            img = img.convert('L').convert('RGB')
        
        # Resize if image exceeds max dimensions (maintain aspect ratio)
        width, height = img.size
        if width > self.settings.max_image_width or height > self.settings.max_image_height:
            ratio = min(
                self.settings.max_image_width / width, 
                self.settings.max_image_height / height
            )
            new_width = int(width * ratio)
            new_height = int(height * ratio)
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        return img
    
    def _optimize_image_from_pil(self, img: Image.Image) -> Image.Image:
        """
        Optimize a PIL Image object (same logic as _optimize_image but for in-memory images)
        
        Args:
            img: PIL Image object
            
        Returns:
            Optimized PIL Image object
        """
        # Convert to RGB if needed
        if img.mode in ('RGBA', 'LA', 'P'):
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            background.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
            img = background
        elif img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Auto-rotate based on EXIF data
        try:
            from PIL import ImageOps
            img = ImageOps.exif_transpose(img)
        except Exception:
            pass
        
        # Auto-crop whitespace if enabled
        if self.settings.enable_auto_crop:
            try:
                gray = img.convert('L')
                bbox = gray.getbbox()
                if bbox:
                    img = img.crop(bbox)
            except Exception:
                pass
        
        # Convert to grayscale if enabled
        if self.settings.enable_grayscale:
            img = img.convert('L').convert('RGB')
        
        # Resize if image exceeds max dimensions
        width, height = img.size
        if width > self.settings.max_image_width or height > self.settings.max_image_height:
            ratio = min(
                self.settings.max_image_width / width,
                self.settings.max_image_height / height
            )
            new_width = int(width * ratio)
            new_height = int(height * ratio)
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        return img
    
    def _encode_optimized_image(self, img: Image.Image) -> str:
        """Encode optimized PIL Image to base64 JPEG string"""
        buffer = io.BytesIO()
        img.save(
            buffer, 
            format='JPEG', 
            quality=self.settings.jpeg_quality, 
            optimize=True
        )
        buffer.seek(0)
        return base64.b64encode(buffer.read()).decode('utf-8')
    
    def _get_image_url_from_pil(self, img: Image.Image) -> ImageUrl:
        """
        Create ImageUrl from a PIL Image object
        
        Args:
            img: PIL Image object
            
        Returns:
            ImageUrl object
        """
        if self._should_optimize_image():
            try:
                optimized_img = self._optimize_image_from_pil(img)
                image_base64 = self._encode_optimized_image(optimized_img)
                data_url = f"data:image/jpeg;base64,{image_base64}"
                return ImageUrl(url=data_url)
            except Exception as e:
                # Fallback to non-optimized
                buffer = io.BytesIO()
                img.save(buffer, format='JPEG', quality=self.settings.jpeg_quality)
                buffer.seek(0)
                image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
                data_url = f"data:image/jpeg;base64,{image_base64}"
                return ImageUrl(url=data_url)
        else:
            # Direct encoding without optimization
            buffer = io.BytesIO()
            img.save(buffer, format='JPEG', quality=self.settings.jpeg_quality)
            buffer.seek(0)
            image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
            data_url = f"data:image/jpeg;base64,{image_base64}"
            return ImageUrl(url=data_url)
    
    def _get_image_url(self, image_path: Path) -> ImageUrl:
        """Create ImageUrl object from image file with optional optimization"""
        if self._should_optimize_image():
            try:
                optimized_img = self._optimize_image(image_path)
                image_base64 = self._encode_optimized_image(optimized_img)
                data_url = f"data:image/jpeg;base64,{image_base64}"
                return ImageUrl(url=data_url)
            except Exception as e:
                # Fallback to original method
                pass
        
        # Original method (no optimization or fallback)
        ext = image_path.suffix.lower()
        image_format_map = {
            '.png': 'png',
            '.jpg': 'jpeg',
            '.jpeg': 'jpeg',
            '.gif': 'gif',
            '.webp': 'webp'
        }
        image_format = image_format_map.get(ext, 'jpeg')
        
        try:
            image_url = ImageUrl.load(
                image_file=str(image_path),
                image_format=image_format
            )
            return image_url
        except Exception:
            # Fallback: create manually
            with open(image_path, "rb") as f:
                image_base64 = base64.b64encode(f.read()).decode('utf-8')
            mime_type = f'image/{image_format}'
            data_url = f"data:{mime_type};base64,{image_base64}"
            return ImageUrl(url=data_url)
    
    def _detect_file_type(self, file_path: Path) -> str:
        """
        Detect if file is PDF or image based on content
        
        Args:
            file_path: Path to the file
            
        Returns:
            'pdf' or 'image'
        """
        try:
            with open(file_path, 'rb') as f:
                header = f.read(12)
            
            # PDF files start with %PDF
            if header.startswith(b'%PDF'):
                return 'pdf'
            
            # Check for image formats
            if (header[:3] == b'\xff\xd8\xff' or  # JPEG
                header[:8] == b'\x89PNG\r\n\x1a\n' or  # PNG
                header[:6] in (b'GIF87a', b'GIF89a') or  # GIF
                (header[:4] == b'RIFF' and header[8:12] == b'WEBP')):  # WebP
                return 'image'
            
            # Fallback: try to open as image
            try:
                img = Image.open(file_path)
                img.verify()
                return 'image'
            except Exception:
                pass
            
            # Fallback: check extension
            ext = file_path.suffix.lower()
            if ext == '.pdf':
                return 'pdf'
            elif ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp', '.tiff']:
                return 'image'
            
            # Default: try as image
            return 'image'
        except Exception:
            # Default: check extension
            ext = file_path.suffix.lower()
            if ext == '.pdf':
                return 'pdf'
            else:
                return 'image'
    
    def _convert_pdf_to_images(self, pdf_path: Path, progress_callback: Optional[Callable] = None) -> List[Image.Image]:
        """
        Convert all pages of a PDF to PIL Image objects
        
        Args:
            pdf_path: Path to the PDF file
            progress_callback: Optional callback function for progress updates
            
        Returns:
            List of PIL Image objects, one per page
            
        Raises:
            Exception: If conversion fails and file is not a valid PDF
        """
        if not PDF_SUPPORT:
            raise ImportError("pdf2image is not installed. Please install it to handle PDFs.")
        
        if progress_callback:
            progress_callback(f"Converting PDF {pdf_path.name} to images...")
        
        try:
            # Use strict=False to handle some PDF syntax errors gracefully
            images = convert_from_path(pdf_path, dpi=200, fmt='RGB', strict=False)
            
            if not images or len(images) == 0:
                raise ValueError("PDF conversion resulted in no images")
            
            if progress_callback:
                progress_callback(f"✅ Converted {len(images)} page(s) from PDF")
            
            return images
        except Exception as e:
            error_msg = f"Failed to convert PDF to images: {str(e)}"
            if progress_callback:
                progress_callback(f"❌ Error: {error_msg}")
            raise Exception(error_msg)
    
    def process_document(
        self, 
        document_path: Path, 
        prompt: str, 
        progress_callback: Optional[Callable] = None
    ) -> Dict:
        """
        Process a single document (image or PDF) with the LLM
        
        Args:
            document_path: Path to the document file (image or PDF)
            prompt: User-provided prompt
            progress_callback: Optional callback function for progress updates
            
        Returns:
            Dictionary with processing results
        """
        if progress_callback:
            progress_callback(f"Processing {document_path.name}...")
        
        try:
            # Detect file type from content, not just extension
            detected_type = self._detect_file_type(document_path)
            is_pdf = detected_type == 'pdf'
            pdf_images = []
            
            if is_pdf:
                if not PDF_SUPPORT:
                    raise ImportError("PDF support is not available. Please install pdf2image.")
                
                try:
                    pdf_images = self._convert_pdf_to_images(document_path, progress_callback)
                    
                    if not pdf_images:
                        raise ValueError("PDF conversion resulted in no images")
                except Exception as pdf_error:
                    # If PDF conversion fails, try treating as image
                    if progress_callback:
                        progress_callback(f"⚠️ PDF conversion failed, trying as image: {str(pdf_error)}")
                    is_pdf = False
                    pdf_images = []
            
            if is_pdf and pdf_images:
                enhanced_prompt = f"""{prompt}

Note: This document has {len(pdf_images)} page(s). Please analyze all pages and extract the relevant information from the page(s) that contain the document data you need. If multiple pages are provided, identify which page contains the main document information and extract from that page."""
                
                if self.model_config.get("requires_image", True):
                    content_items = [TextContentItem(text=enhanced_prompt)]
                    
                    for idx, pdf_image in enumerate(pdf_images, 1):
                        if progress_callback:
                            progress_callback(f"Preparing page {idx}/{len(pdf_images)} for LLM...")
                        image_url = self._get_image_url_from_pil(pdf_image)
                        content_items.append(ImageContentItem(image_url=image_url))
                    
                    user_message = UserMessage(content=content_items)
                else:
                    user_message = UserMessage(content=enhanced_prompt)
            else:
                # Process as image
                if self.model_config.get("requires_image", True):
                    image_url = self._get_image_url(document_path)
                    content_items = [
                        TextContentItem(text=prompt),
                        ImageContentItem(image_url=image_url)
                    ]
                    user_message = UserMessage(content=content_items)
                else:
                    user_message = UserMessage(content=prompt)
            
            messages = [
                SystemMessage("You are a helpful document analysis assistant."),
                user_message
            ]
            
            if progress_callback:
                progress_callback(f"Sending request to {self.model_name}...")
            
            # Threading-based timeout wrapper
            response = None
            exception_container = [None]
            
            def api_call():
                try:
                    result = self.client.complete(
                        messages=messages,
                        model=self.model_config["model_id"],
                        temperature=self.settings.default_temperature,
                        max_tokens=self.settings.default_max_tokens,
                        stream=False
                    )
                    exception_container[0] = result
                except Exception as e:
                    exception_container[0] = e
            
            api_thread = threading.Thread(target=api_call, daemon=True)
            api_thread.start()
            api_thread.join(timeout=self.settings.api_timeout_seconds)
            
            if api_thread.is_alive():
                error_msg = f"API call timed out after {self.settings.api_timeout_seconds} seconds"
                if progress_callback:
                    progress_callback(f"❌ Error: {error_msg}")
                return {
                    "success": False,
                    "error": error_msg,
                    "document_path": str(document_path),
                    "model": self.model_name,
                    "prompt": prompt
                }
            
            if isinstance(exception_container[0], Exception):
                raise exception_container[0]
            
            response = exception_container[0]
            
            if response.choices and len(response.choices) > 0:
                content = response.choices[0].message.content
                
                result = {
                    "success": True,
                    "content": content,
                    "document_path": str(document_path),
                    "model": self.model_name,
                    "prompt": prompt,
                    "is_pdf": is_pdf and len(pdf_images) > 0,
                    "pages_processed": len(pdf_images) if (is_pdf and pdf_images) else 1
                }
                
                if progress_callback:
                    progress_callback(f"✅ Completed {document_path.name}")
                
                return result
            else:
                raise ValueError("No response content received from model")
                
        except HttpResponseError as e:
            # Provide more helpful error messages
            if e.status_code == 401:
                error_msg = f"Authentication failed (401): GITHUB_TOKEN is invalid or expired. Please check your .env file and ensure GITHUB_TOKEN is set correctly."
            else:
                error_msg = f"HTTP Error {e.status_code}: {e.message}"
            if progress_callback:
                progress_callback(f"❌ Error: {error_msg}")
            return {
                "success": False,
                "error": error_msg,
                "document_path": str(document_path),
                "model": self.model_name,
                "prompt": prompt
            }
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            if progress_callback:
                progress_callback(f"❌ Error: {error_msg}")
            return {
                "success": False,
                "error": error_msg,
                "document_path": str(document_path),
                "model": self.model_name,
                "prompt": prompt
            }
    
    def close(self):
        """Close the client connection"""
        if self.client:
            self.client.close()

