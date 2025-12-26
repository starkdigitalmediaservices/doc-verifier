"""
File handling utilities
For downloading and managing documents
"""

import re
import httpx
import aiofiles
from pathlib import Path
from typing import Optional, Tuple
from urllib.parse import urlparse, parse_qs


def save_file(content: bytes, save_path: Path) -> Path:
    """
    Save file content to disk
    
    Args:
        content: File content as bytes
        save_path: Path to save the file
        
    Returns:
        Path to saved file
    """
    save_path.parent.mkdir(parents=True, exist_ok=True)
    save_path.write_bytes(content)
    return save_path


def convert_google_drive_link(url: str) -> str:
    """
    Convert Google Drive sharing link to direct download link
    
    Supports multiple Google Drive URL formats:
    - https://drive.google.com/file/d/FILE_ID/view?usp=sharing
    - https://drive.google.com/open?id=FILE_ID
    - https://drive.google.com/uc?id=FILE_ID (already direct)
    
    Args:
        url: Google Drive sharing URL
        
    Returns:
        Direct download URL for Google Drive with confirm parameter to bypass virus scan,
        or original URL if not a Google Drive link
    """
    # Pattern 1: /file/d/FILE_ID/view
    match = re.search(r'/file/d/([a-zA-Z0-9_-]+)', url)
    if match:
        file_id = match.group(1)
        # Use confirm=t to bypass virus scan warning for large files
        return f"https://drive.google.com/uc?export=download&id={file_id}&confirm=t"
    
    # Pattern 2: /open?id=FILE_ID or /uc?id=FILE_ID
    parsed = urlparse(url)
    if 'drive.google.com' in parsed.netloc:
        query_params = parse_qs(parsed.query)
        if 'id' in query_params:
            file_id = query_params['id'][0]
            return f"https://drive.google.com/uc?export=download&id={file_id}&confirm=t"
    
    # Not a Google Drive link or already in correct format
    return url


async def download_file(url: str, save_path: Path) -> Path:
    """
    Download a file from URL and save to local path
    
    Automatically converts Google Drive sharing links to direct download links.
    Handles Google Drive virus scan warnings for large files.
    
    Args:
        url: URL to download from
        save_path: Path to save the file
        
    Returns:
        Path to saved file
        
    Raises:
        Exception: If download fails or file is not a valid document
    """
    # Convert Google Drive links to direct download links
    url = convert_google_drive_link(url)
    
    async with httpx.AsyncClient(timeout=120.0, follow_redirects=True) as client:
        # For Google Drive, first check if we get HTML (virus scan warning)
        if 'drive.google.com' in url:
            try:
                # Make a small request to check content type
                test_response = await client.get(url, headers={'Range': 'bytes=0-1023'})
                content_type = test_response.headers.get('content-type', '').lower()
                
                if 'text/html' in content_type:
                    # Check if response is HTML
                    content_preview = test_response.text[:500].lower()
                    if '<html' in content_preview or '<!doctype' in content_preview:
                        raise ValueError(
                            "Failed to download from Google Drive. The file may require permission "
                            "or be too large. Please ensure the file is publicly accessible with "
                            "'Anyone with the link' permission. Alternatively, try downloading the file "
                            "manually and using a direct file hosting service."
                        )
            except ValueError:
                raise  # Re-raise our custom error
            except Exception:
                pass  # Continue with full download
        
        # Download the full file
        async with client.stream('GET', url) as response:
            response.raise_for_status()
            
            # Ensure parent directory exists
            save_path.parent.mkdir(parents=True, exist_ok=True)
            
            async with aiofiles.open(save_path, 'wb') as f:
                async for chunk in response.aiter_bytes():
                    await f.write(chunk)
    
    # Detect actual file type and correct extension if needed
    file_type, correct_ext = detect_file_type(save_path)
    if file_type != 'unknown' and correct_ext:
        current_ext = save_path.suffix.lower()
        # If extension is missing or incorrect, rename with correct extension
        if not current_ext or current_ext != correct_ext:
            # If file has no extension, add it; otherwise replace it
            if not current_ext:
                new_path = save_path.with_suffix(correct_ext)
            else:
                new_path = save_path.with_suffix(correct_ext)
            save_path.rename(new_path)
            return new_path
    
    return save_path


def detect_file_type(file_path: Path) -> Tuple[str, str]:
    """
    Detect file type from file content using magic bytes
    
    Args:
        file_path: Path to the file
        
    Returns:
        Tuple of (file_type, extension) where:
        - file_type: 'pdf', 'image', or 'unknown'
        - extension: Appropriate file extension (e.g., '.pdf', '.jpg', '.png')
    """
    if not file_path.exists():
        return ('unknown', '')
    
    try:
        # Read first 12 bytes for magic number detection
        with open(file_path, 'rb') as f:
            header = f.read(12)
        
        if len(header) < 3:
            return ('unknown', '')
        
        # PDF files start with %PDF
        if header.startswith(b'%PDF'):
            return ('pdf', '.pdf')
        
        # JPEG files start with FF D8 FF
        if header[:3] == b'\xff\xd8\xff':
            return ('image', '.jpg')
        
        # PNG files start with 89 50 4E 47 0D 0A 1A 0A
        if len(header) >= 8 and header[:8] == b'\x89PNG\r\n\x1a\n':
            return ('image', '.png')
        
        # GIF files start with GIF87a or GIF89a
        if len(header) >= 6 and header[:6] in (b'GIF87a', b'GIF89a'):
            return ('image', '.gif')
        
        # WebP files start with RIFF and contain WEBP
        if len(header) >= 12 and header[:4] == b'RIFF' and header[8:12] == b'WEBP':
            return ('image', '.webp')
        
        # Try to open as image with PIL as fallback
        try:
            from PIL import Image
            img = Image.open(file_path)
            img.verify()
            # Determine extension from PIL format
            format_to_ext = {
                'JPEG': '.jpg',
                'PNG': '.png',
                'GIF': '.gif',
                'WEBP': '.webp',
                'BMP': '.bmp',
                'TIFF': '.tiff'
            }
            ext = format_to_ext.get(img.format, '.jpg')
            return ('image', ext)
        except Exception:
            pass
        
        # Try to open as PDF with pypdf as fallback
        try:
            import pypdf
            with open(file_path, 'rb') as f:
                pdf_reader = pypdf.PdfReader(f)
                if len(pdf_reader.pages) > 0:
                    return ('pdf', '.pdf')
        except Exception:
            pass
        
        return ('unknown', '')
    except Exception:
        return ('unknown', '')


def get_file_extension(filename: str) -> str:
    """
    Get file extension from filename
    
    Args:
        filename: Filename or URL
        
    Returns:
        File extension (e.g., '.jpg', '.pdf')
    """
    # Handle URLs
    if filename.startswith('http'):
        parsed = urlparse(filename)
        filename = parsed.path
    
    # Get extension
    path = Path(filename)
    return path.suffix.lower()

