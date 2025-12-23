"""
ComfyUI Metadata Nodes
Professional EXIF, XMP, and IPTC metadata workflows for ComfyUI

Author: Kevin Green
License: MIT
"""

from .ffpy_add_xmp_node import FFpyAddXMPNode
from .ffpy_load_image_folder_node import FFpyLoadImageFolderNode
from .ffpy_exiftool_node import FFpyExifToolNode

NODE_CLASS_MAPPINGS = {
    "FFpyAddXMPNode": FFpyAddXMPNode,
    "FFpyLoadImageFolderNode": FFpyLoadImageFolderNode,
    "FFpyExifToolNode": FFpyExifToolNode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "FFpyAddXMPNode": "FFpy Add XMP to Image",
    "FFpyLoadImageFolderNode": "FFpy Load Image from Folder",
    "FFpyExifToolNode": "FFpy ExifTool (Advanced Metadata)",
}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
