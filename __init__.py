"""
ComfyUI Metadata Nodes
Professional EXIF, XMP, and IPTC metadata workflows for ComfyUI

Author: Kevin Green
License: MIT
"""

from .ffpy_save_with_metadata_node import FFpySaveWithMetadataNode
from .ffpy_load_image_folder_node import FFpyLoadImageFolderNode
from .ffpy_exiftool_node import FFpyExifToolNode

NODE_CLASS_MAPPINGS = {
    "FFpySaveWithMetadataNode": FFpySaveWithMetadataNode,
    "FFpyLoadImageFolderNode": FFpyLoadImageFolderNode,
    "FFpyExifToolNode": FFpyExifToolNode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "FFpySaveWithMetadataNode": "FFpy Save with Metadata",
    "FFpyLoadImageFolderNode": "FFpy Load Image from Folder",
    "FFpyExifToolNode": "FFpy ExifTool (Advanced Metadata)",
}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
