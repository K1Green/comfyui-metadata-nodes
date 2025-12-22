"""
FFpy Load Image from Folder Node

Load images from a folder while preserving metadata access.
Perfect for use with FFpy ExifTool to read comprehensive metadata.
"""

from __future__ import annotations
import os
import numpy as np
import torch
from PIL import Image
from pathlib import Path
from typing import Optional, List, Tuple
import logging

logger = logging.getLogger(__name__)


class FFpyLoadImageFolderNode:
    """
    Load images from a folder with metadata preservation.

    Returns both the image tensor and file path, allowing:
    - Image processing in ComfyUI
    - Metadata reading with FFpy ExifTool from original file
    """

    RETURN_TYPES = ("IMAGE", "STRING", "STRING", "STRING", "INT")
    RETURN_NAMES = ("image", "file_path", "filename", "debug_log", "total_images")
    FUNCTION = "load_image"
    CATEGORY = "api node/photoshop"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "folder_path": (
                    "STRING",
                    {
                        "default": "/Users/kevin/Applications/Development/ComfyUI/output",
                        "multiline": False,
                        "tooltip": "Full path to folder containing images",
                    },
                ),
                "image_index": (
                    "INT",
                    {
                        "default": 0,
                        "min": 0,
                        "max": 99999,
                        "tooltip": "Which image to load (0 = first, 1 = second, etc.)",
                    },
                ),
            },
            "optional": {
                "file_pattern": (
                    "STRING",
                    {
                        "default": "*.png,*.jpg,*.jpeg",
                        "multiline": False,
                        "tooltip": "File patterns to match (comma-separated, e.g., '*.png,*.jpg')",
                    },
                ),
                "sort_by": (
                    ["name", "date_modified", "date_created", "size"],
                    {
                        "default": "date_modified",
                        "tooltip": "How to sort the images in the folder",
                    },
                ),
                "sort_order": (
                    ["ascending", "descending"],
                    {
                        "default": "descending",
                        "tooltip": "Sort order (descending = newest/largest first)",
                    },
                ),
                "recursive": (
                    "BOOLEAN",
                    {
                        "default": False,
                        "tooltip": "Search subfolders recursively",
                    },
                ),
            },
        }

    def load_image(
        self,
        folder_path: str,
        image_index: int = 0,
        file_pattern: str = "*.png,*.jpg,*.jpeg",
        sort_by: str = "date_modified",
        sort_order: str = "descending",
        recursive: bool = False,
    ) -> Tuple[torch.Tensor, str, str, str, int]:
        """
        Load image from folder with metadata preservation.
        """

        # Build initial debug log
        debug_log = self._build_debug_log_start(folder_path, file_pattern, sort_by, recursive)

        try:
            # Validate folder path
            folder = Path(folder_path)
            if not folder.exists():
                raise ValueError(f"Folder does not exist: {folder_path}")
            if not folder.is_dir():
                raise ValueError(f"Path is not a folder: {folder_path}")

            # Get list of image files
            image_files = self._get_image_files(folder, file_pattern, recursive)

            if not image_files:
                raise ValueError(f"No images found in folder: {folder_path}\nPattern: {file_pattern}")

            # Sort images
            image_files = self._sort_files(image_files, sort_by, sort_order)

            total_images = len(image_files)

            # Validate index
            if image_index < 0 or image_index >= total_images:
                raise ValueError(
                    f"Image index {image_index} out of range. Folder contains {total_images} images (indices 0-{total_images-1})"
                )

            # Get selected file
            selected_file = image_files[image_index]
            file_path_str = str(selected_file.absolute())
            filename = selected_file.name

            # Load image
            img = Image.open(selected_file)

            # Convert to RGB if necessary (handles RGBA, L, etc.)
            if img.mode == 'RGBA':
                # Keep alpha channel for RGBA images
                img_array = np.array(img).astype(np.float32) / 255.0
            elif img.mode != 'RGB':
                # Convert other modes to RGB
                img = img.convert('RGB')
                img_array = np.array(img).astype(np.float32) / 255.0
            else:
                img_array = np.array(img).astype(np.float32) / 255.0

            # Convert to tensor [1, H, W, C]
            image_tensor = torch.from_numpy(img_array)[None,]

            # Build final debug log
            debug_log += self._build_debug_log_success(
                selected_file, image_index, total_images, img, sort_by
            )

            logger.info(f"Loaded image: {filename} ({image_index+1}/{total_images})")

            return (image_tensor, file_path_str, filename, debug_log, total_images)

        except Exception as e:
            error_msg = f"\n[ERROR] Failed to load image: {str(e)}\n"
            error_msg += "======================================================="
            logger.error(f"Image load error: {e}")

            # Return blank image on error
            blank = torch.zeros((1, 512, 512, 3))
            return (blank, "", "", debug_log + error_msg, 0)

    def _get_image_files(
        self,
        folder: Path,
        file_pattern: str,
        recursive: bool,
    ) -> List[Path]:
        """Get list of image files matching pattern."""

        # Parse patterns (comma-separated)
        patterns = [p.strip() for p in file_pattern.split(",") if p.strip()]

        image_files = []

        for pattern in patterns:
            if recursive:
                # Search recursively
                image_files.extend(folder.rglob(pattern))
            else:
                # Search only in folder
                image_files.extend(folder.glob(pattern))

        # Remove duplicates and sort by path
        image_files = sorted(set(image_files))

        # Filter to only existing files
        image_files = [f for f in image_files if f.is_file()]

        return image_files

    def _sort_files(
        self,
        files: List[Path],
        sort_by: str,
        sort_order: str,
    ) -> List[Path]:
        """Sort files according to criteria."""

        reverse = (sort_order == "descending")

        if sort_by == "name":
            sorted_files = sorted(files, key=lambda f: f.name.lower(), reverse=reverse)
        elif sort_by == "date_modified":
            sorted_files = sorted(files, key=lambda f: f.stat().st_mtime, reverse=reverse)
        elif sort_by == "date_created":
            sorted_files = sorted(files, key=lambda f: f.stat().st_ctime, reverse=reverse)
        elif sort_by == "size":
            sorted_files = sorted(files, key=lambda f: f.stat().st_size, reverse=reverse)
        else:
            sorted_files = files

        return sorted_files

    def _build_debug_log_start(
        self,
        folder_path: str,
        file_pattern: str,
        sort_by: str,
        recursive: bool,
    ) -> str:
        """Build initial debug log in Firefly style."""
        log = "=" * 55 + "\n"
        log += "LOCAL Image Loading from Folder\n"
        log += "-" * 55 + "\n"
        log += "Operation: Load image with metadata preservation\n"
        log += "Method: Direct file access (PIL)\n"
        log += f"\nFolder Settings:\n"
        log += f"  path: {folder_path}\n"
        log += f"  pattern: {file_pattern}\n"
        log += f"  sort_by: {sort_by}\n"
        log += f"  recursive: {recursive}\n"
        log += "=" * 55 + "\n"
        log += "Scanning folder for images...\n"
        return log

    def _build_debug_log_success(
        self,
        file_path: Path,
        index: int,
        total: int,
        img: Image.Image,
        sort_by: str,
    ) -> str:
        """Build success section of debug log."""

        stat = file_path.stat()

        log = f"\nFound {total} image(s) in folder\n"
        log += f"Sorted by: {sort_by}\n"
        log += f"\n" + "=" * 55 + "\n"
        log += f"Loading image {index + 1} of {total}...\n"
        log += f"\n[OK] Image loaded successfully\n"
        log += f"  File: {file_path.name}\n"
        log += f"  Path: {file_path.parent}\n"
        log += f"  Size: {stat.st_size / 1024:.2f} KB\n"
        log += f"  Dimensions: {img.width}x{img.height}\n"
        log += f"  Mode: {img.mode}\n"
        log += f"  Format: {img.format or 'Unknown'}\n"
        log += f"\n[INFO] Use file_path output with FFpy ExifTool\n"
        log += f"       to read comprehensive metadata\n"
        log += "=" * 55 + "\n"

        return log


# Export for ComfyUI
NODE_CLASS_MAPPINGS = {
    "FFpyLoadImageFolderNode": FFpyLoadImageFolderNode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "FFpyLoadImageFolderNode": "FFpy Load Image from Folder",
}
