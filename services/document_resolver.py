"""
Document Resolver Service
Resolves document content from multiple sources: download_url, file_buffer (base64), or uploaded file.
"""

import base64
import time
from pathlib import Path
from typing import Optional, Tuple

from utils.file_handler import download_file, get_file_extension, save_file, detect_file_type


async def resolve_document_file(
    doc_info: dict,
    temp_dir: Path,
    uploaded_file=None,
) -> Tuple[Path, str]:
    """
    Resolve document to a local file path from one of three sources.

    Args:
        doc_info: Document info dict with one of:
            - download_url: URL to download from
            - file_buffer: Base64-encoded file content
            - file_path: Path to already-saved file (from multipart upload)
        temp_dir: Temporary directory for saving files
        uploaded_file: Optional uploaded file object (FastAPI UploadFile)
            Used when file is browsed from frontend via multipart form.

    Returns:
        Tuple of (file_path, document_source) where document_source is used for
        display in results (e.g., URL string or "uploaded file").

    Raises:
        ValueError: If no valid document source is provided
    """
    download_url = doc_info.get("download_url")
    file_buffer = doc_info.get("file_buffer")
    file_path = doc_info.get("file_path")

    if download_url:
        # Source 1: Download from URL
        file_ext = get_file_extension(str(download_url))
        if not file_ext:
            file_ext = ""
        temp_file = temp_dir / f"doc_{int(time.time())}{file_ext}"
        actual_file_path = await download_file(str(download_url), temp_file)
        return actual_file_path, str(download_url)

    elif file_buffer:
        # Source 2: Base64-encoded buffer
        try:
            file_content = base64.b64decode(file_buffer)
        except Exception as e:
            raise ValueError(f"Invalid base64 file_buffer: {e}") from e

        file_ext = ""
        temp_file = temp_dir / f"doc_{int(time.time())}{file_ext}"
        actual_file_path = save_file(file_content, temp_file)

        # Detect and correct extension
        file_type, correct_ext = detect_file_type(actual_file_path)
        if file_type != "unknown" and correct_ext:
            new_path = actual_file_path.with_suffix(correct_ext)
            actual_file_path.rename(new_path)
            actual_file_path = new_path

        return actual_file_path, "base64_buffer"

    elif file_path:
        # Source 3: File already saved (from multipart upload in API route)
        path = Path(file_path)
        if not path.exists():
            raise ValueError(f"File path does not exist: {file_path}")
        return path, str(file_path)

    elif uploaded_file:
        # Source 4: Uploaded file object (used when called from API route with multipart)
        file_content = await uploaded_file.read()
        file_ext = _get_extension_from_filename(uploaded_file.filename)
        temp_file = temp_dir / f"doc_{int(time.time())}{file_ext}"
        actual_file_path = save_file(file_content, temp_file)

        # Detect and correct extension
        file_type, correct_ext = detect_file_type(actual_file_path)
        if file_type != "unknown" and correct_ext:
            new_path = actual_file_path.with_suffix(correct_ext)
            actual_file_path.rename(new_path)
            actual_file_path = new_path

        return actual_file_path, uploaded_file.filename or "uploaded_file"

    else:
        raise ValueError(
            "No document source provided. Provide one of: download_url, file_buffer, "
            "file_path, or uploaded_file"
        )


def _get_extension_from_filename(filename: Optional[str]) -> str:
    """Get file extension from filename."""
    if not filename:
        return ""
    return Path(filename).suffix.lower()
