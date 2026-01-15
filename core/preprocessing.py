"""
Modular Preprocessing Pipeline
Supports multiple preprocessing modes:
- 0: No preprocessing
- 1: Token optimization (resize/compress for token reduction)
- 2: Quality enhancement (AI-powered quality improvement)
"""

from enum import IntEnum
from pathlib import Path
from typing import Optional
from PIL import Image
import numpy as np
import cv2

from config import Settings


class PreprocessingMode(IntEnum):
    """Preprocessing mode enumeration"""
    NONE = 0  # No preprocessing
    TOKEN_OPTIMIZATION = 1  # Resize/compress for token reduction
    QUALITY_ENHANCEMENT = 2  # AI-powered quality enhancement


class PreprocessingPipeline:
    """Modular preprocessing pipeline that routes to appropriate preprocessor"""
    
    def __init__(self, settings: Optional[Settings] = None):
        """
        Initialize preprocessing pipeline
        
        Args:
            settings: Settings instance (if None, uses get_settings())
        """
        from config import get_settings
        self.settings = settings or get_settings()
        self._quality_enhancer = None
    
    def _get_quality_enhancer(self):
        """Lazy load quality enhancer to avoid import errors if dependencies missing"""
        if self._quality_enhancer is None:
            try:
                from document_preprocessor import ImageEnhancer
                self._quality_enhancer = ImageEnhancer()
            except ImportError as e:
                raise ImportError(
                    "Quality enhancement requires document_preprocessor module. "
                    "Ensure all dependencies are installed: "
                    "opencv-python, scikit-image, pillow"
                ) from e
        return self._quality_enhancer
    
    def pil_to_numpy(self, pil_image: Image.Image) -> np.ndarray:
        """
        Convert PIL Image to numpy array (BGR format for OpenCV)
        
        Args:
            pil_image: PIL Image object
            
        Returns:
            numpy array in BGR format
        """
        # Convert PIL to numpy (RGB)
        np_img = np.array(pil_image)
        
        # Convert RGB to BGR for OpenCV
        if len(np_img.shape) == 3:
            np_img = cv2.cvtColor(np_img, cv2.COLOR_RGB2BGR)
        
        return np_img
    
    def numpy_to_pil(self, np_image: np.ndarray) -> Image.Image:
        """
        Convert numpy array to PIL Image
        
        Args:
            np_image: numpy array (BGR or grayscale)
            
        Returns:
            PIL Image object
        """
        # Ensure uint8
        if np_image.dtype != np.uint8:
            np_image = np.clip(np_image, 0, 255).astype(np.uint8)
        
        # Convert BGR to RGB if needed
        if len(np_image.shape) == 3:
            rgb_image = cv2.cvtColor(np_image, cv2.COLOR_BGR2RGB)
            return Image.fromarray(rgb_image)
        else:
            return Image.fromarray(np_image)
    
    def apply_token_optimization(self, image: Image.Image) -> Image.Image:
        """
        Apply token optimization preprocessing (resize/compress)
        This is the original preprocessing logic
        
        Args:
            image: PIL Image object
            
        Returns:
            Optimized PIL Image object
        """
        # Convert to RGB if needed (for JPEG compatibility)
        if image.mode in ('RGBA', 'LA', 'P'):
            background = Image.new('RGB', image.size, (255, 255, 255))
            if image.mode == 'P':
                image = image.convert('RGBA')
            background.paste(image, mask=image.split()[-1] if image.mode in ('RGBA', 'LA') else None)
            image = background
        elif image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Auto-rotate based on EXIF data
        try:
            from PIL import ImageOps
            image = ImageOps.exif_transpose(image)
        except Exception:
            pass
        
        # Auto-crop whitespace if enabled
        if self.settings.enable_auto_crop:
            try:
                gray = image.convert('L')
                bbox = gray.getbbox()
                if bbox:
                    image = image.crop(bbox)
            except Exception:
                pass
        
        # Convert to grayscale if enabled
        if self.settings.enable_grayscale:
            image = image.convert('L').convert('RGB')
        
        # Resize if image exceeds max dimensions (maintain aspect ratio)
        width, height = image.size
        if width > self.settings.max_image_width or height > self.settings.max_image_height:
            ratio = min(
                self.settings.max_image_width / width,
                self.settings.max_image_height / height
            )
            new_width = int(width * ratio)
            new_height = int(height * ratio)
            image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        return image
    
    def apply_quality_enhancement(self, image: Image.Image) -> Image.Image:
        """
        Apply quality enhancement preprocessing (AI-powered)
        Uses the new document_preprocessor pipeline
        
        Args:
            image: PIL Image object
            
        Returns:
            Enhanced PIL Image object
        """
        # Convert PIL to numpy (BGR)
        np_image = self.pil_to_numpy(image)
        
        # Apply quality enhancement
        enhancer = self._get_quality_enhancer()
        result = enhancer.process(np_image, method='auto')
        
        # Get enhanced image
        enhanced_np = result['enhanced_image']
        
        # Convert back to PIL
        enhanced_pil = self.numpy_to_pil(enhanced_np)
        
        # Convert to RGB if needed (for JPEG compatibility)
        if enhanced_pil.mode != 'RGB':
            enhanced_pil = enhanced_pil.convert('RGB')
        
        return enhanced_pil
    
    def preprocess(self, image: Image.Image, mode: PreprocessingMode) -> Image.Image:
        """
        Apply preprocessing based on mode
        
        Args:
            image: PIL Image object
            mode: PreprocessingMode enum value
            
        Returns:
            Preprocessed PIL Image object
        """
        if mode == PreprocessingMode.NONE:
            # No preprocessing - just ensure RGB format
            if image.mode != 'RGB':
                if image.mode in ('RGBA', 'LA', 'P'):
                    background = Image.new('RGB', image.size, (255, 255, 255))
                    if image.mode == 'P':
                        image = image.convert('RGBA')
                    background.paste(image, mask=image.split()[-1] if image.mode in ('RGBA', 'LA') else None)
                    return background
                else:
                    return image.convert('RGB')
            return image
        
        elif mode == PreprocessingMode.TOKEN_OPTIMIZATION:
            return self.apply_token_optimization(image)
        
        elif mode == PreprocessingMode.QUALITY_ENHANCEMENT:
            return self.apply_quality_enhancement(image)
        
        else:
            # Unknown mode - return original
            return image
    
    def preprocess_from_path(self, image_path: Path, mode: PreprocessingMode) -> Image.Image:
        """
        Load image from path and apply preprocessing
        
        Args:
            image_path: Path to image file
            mode: PreprocessingMode enum value
            
        Returns:
            Preprocessed PIL Image object
        """
        image = Image.open(image_path)
        return self.preprocess(image, mode)
