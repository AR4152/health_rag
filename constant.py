"""Constants for the package.

This file defines:
- SUPPORTED_IMAGE_TYPES: File extensions for supported image formats for context creation.
- SUPPORTED_FILE_TYPES: File extensions for all supported file types for context creation.
"""

SUPPORTED_IMAGE_TYPES = {".png", ".jpg", ".jpeg", ".tiff", ".bmp"}
"""Set of supported image file extensions for context creation."""

SUPPORTED_FILE_TYPES = {
    ".pdf",
    ".txt",
    ".docx",
    ".md",
    ".csv",
    ".eml",
    ".xlsx",
    ".xls",
} | SUPPORTED_IMAGE_TYPES
"""Set of all supported file extensions for context creation."""
