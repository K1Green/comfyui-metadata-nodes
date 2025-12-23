"""
FFpy Add XMP to Image Node

Adds XMP metadata to images and saves them with embedded metadata.
Embeds title, description, keywords, creator, copyright, and other metadata directly into PNG files.
"""

from __future__ import annotations
import os
import numpy as np
import torch
from PIL import Image
from PIL.PngImagePlugin import PngInfo
import json
from datetime import datetime
from pathlib import Path
import folder_paths
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)


class FFpyAddXMPNode:
    """
    Add XMP metadata to images and save with embedded metadata.

    This node embeds XMP metadata directly into PNG files, preserving
    title, description, keywords, creator, copyright, and other metadata.
    """

    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("file_path", "debug_log")
    FUNCTION = "save_with_metadata"
    CATEGORY = "image/metadata"
    OUTPUT_NODE = True

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE", {"tooltip": "Image to save"}),
                "filename_prefix": (
                    "STRING",
                    {
                        "default": "ComfyUI",
                        "tooltip": "Filename prefix (will add timestamp and counter)",
                    },
                ),
            },
            "optional": {
                "title": (
                    "STRING",
                    {
                        "default": "",
                        "multiline": False,
                        "tooltip": "Image title (dc:title)",
                    },
                ),
                "description": (
                    "STRING",
                    {
                        "default": "",
                        "multiline": True,
                        "tooltip": "Image description (dc:description)",
                    },
                ),
                "keywords": (
                    "STRING",
                    {
                        "default": "",
                        "multiline": False,
                        "tooltip": "Comma-separated keywords (dc:subject)",
                    },
                ),
                "creator": (
                    "STRING",
                    {
                        "default": "",
                        "multiline": False,
                        "tooltip": "Creator/Artist name (dc:creator)",
                    },
                ),
                "copyright": (
                    "STRING",
                    {
                        "default": "",
                        "multiline": False,
                        "tooltip": "Copyright notice (dc:rights)",
                    },
                ),
                "rating": (
                    "INT",
                    {
                        "default": 0,
                        "min": 0,
                        "max": 5,
                        "tooltip": "Rating 0-5 stars (xmp:Rating)",
                    },
                ),
                "label": (
                    ["None", "Red", "Yellow", "Green", "Blue", "Purple"],
                    {
                        "default": "None",
                        "tooltip": "Color label (xmp:Label)",
                    },
                ),
                "custom_metadata": (
                    "STRING",
                    {
                        "default": "",
                        "multiline": True,
                        "tooltip": "Custom JSON metadata (optional)",
                    },
                ),
                "output_path": (
                    "STRING",
                    {
                        "default": "",
                        "multiline": False,
                        "tooltip": "Optional: specific output directory (leave empty for ComfyUI default output folder)",
                    },
                ),
            },
        }

    def save_with_metadata(
        self,
        image: torch.Tensor,
        filename_prefix: str = "ComfyUI",
        title: str = "",
        description: str = "",
        keywords: str = "",
        creator: str = "",
        copyright: str = "",
        rating: int = 0,
        label: str = "None",
        custom_metadata: str = "",
        output_path: str = "",
    ) -> tuple[str, str]:
        """
        Save image with embedded XMP metadata.
        """

        # Build initial debug log
        debug_log = self._build_debug_log(
            filename_prefix, title, description, keywords, creator, copyright, rating, label, custom_metadata, output_path
        )

        try:
            # Determine output directory
            if output_path and output_path.strip():
                output_dir = Path(output_path.strip())
                output_dir.mkdir(parents=True, exist_ok=True)
            else:
                # Use ComfyUI's default output folder
                output_dir = Path(folder_paths.get_output_directory())

            # Generate filename with timestamp and counter
            counter = 1
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

            while True:
                filename = f"{filename_prefix}_{timestamp}_{counter:05d}.png"
                file_path = output_dir / filename
                if not file_path.exists():
                    break
                counter += 1

            # Convert tensor to PIL Image
            i = 255.0 * image[0].cpu().numpy()
            img_pil = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))

            # Build XMP metadata
            xmp_data = self._build_xmp_metadata(
                title, description, keywords, creator, copyright, rating, label, custom_metadata
            )

            # Create PNG info with metadata
            pnginfo = PngInfo()

            # Add standard metadata fields
            if title:
                pnginfo.add_text("Title", title)
            if description:
                pnginfo.add_text("Description", description)
            if creator:
                pnginfo.add_text("Author", creator)
            if copyright:
                pnginfo.add_text("Copyright", copyright)

            # Add XMP as JSON
            pnginfo.add_text("XMP", json.dumps(xmp_data, indent=2, ensure_ascii=False))

            # Add ComfyUI marker
            pnginfo.add_text("ComfyUI_XMP_Node", "FFpySaveWithMetadataNode")
            pnginfo.add_text("Software", "ComfyUI with FFpy Metadata Nodes")

            # Save image with metadata
            img_pil.save(str(file_path), format="PNG", pnginfo=pnginfo, compress_level=4)

            logger.info(f"Saved image with metadata: {file_path}")

            # Update debug log with success
            debug_log += f"\n{'='*55}\n"
            debug_log += f"Saving image with metadata...\n"
            debug_log += f"\n[OK] Image saved successfully\n"
            debug_log += f"  File: {file_path.name}\n"
            debug_log += f"  Path: {file_path.parent}\n"
            debug_log += f"  Size: {file_path.stat().st_size / 1024:.2f} KB\n"
            debug_log += f"{'='*55}\n"

            return (str(file_path), debug_log)

        except Exception as e:
            error_msg = f"\n{'='*55}\n"
            error_msg += f"[ERROR] Failed to save image with metadata\n"
            error_msg += f"  Error: {str(e)}\n"
            error_msg += f"{'='*55}\n"
            logger.error(f"Failed to save image with metadata: {e}")
            debug_log += error_msg
            raise Exception(f"Failed to save image with metadata: {str(e)}")

    def _build_debug_log(
        self,
        filename_prefix: str,
        title: str,
        description: str,
        keywords: str,
        creator: str,
        copyright: str,
        rating: int,
        label: str,
        custom_metadata: str,
        output_path: str,
    ) -> str:
        """Build formatted debug log in Firefly style."""
        log = "=" * 55 + "\n"
        log += "LOCAL Image Save with XMP Metadata\n"
        log += "-" * 55 + "\n"
        log += "Operation: Save image with embedded XMP metadata\n"
        log += "Method: Local (Python PIL)\n"
        log += f"\nFile Settings:\n"
        log += f"  filename_prefix: {filename_prefix}\n"
        log += f"  output_path: {output_path if output_path else '[ComfyUI default output folder]'}\n"
        log += f"  format: PNG\n"
        log += f"\nMetadata Fields:\n"

        metadata_count = 0
        if title:
            log += f"  title: {title}\n"
            metadata_count += 1
        if description:
            desc_preview = description[:50] + "..." if len(description) > 50 else description
            log += f"  description: {desc_preview}\n"
            metadata_count += 1
        if keywords:
            log += f"  keywords: {keywords}\n"
            metadata_count += 1
        if creator:
            log += f"  creator: {creator}\n"
            metadata_count += 1
        if copyright:
            log += f"  copyright: {copyright}\n"
            metadata_count += 1
        if rating > 0:
            log += f"  rating: {rating}/5 stars\n"
            metadata_count += 1
        if label != "None":
            log += f"  label: {label}\n"
            metadata_count += 1
        if custom_metadata and custom_metadata.strip():
            log += f"  custom_metadata: [JSON data provided]\n"
            metadata_count += 1

        if metadata_count == 0:
            log += "  [No metadata provided - saving without XMP]\n"
        else:
            log += f"\nTotal metadata fields: {metadata_count}\n"

        log += "=" * 55 + "\n"
        log += "Preparing to save...\n"

        return log

    def _build_xmp_metadata(
        self,
        title: str,
        description: str,
        keywords: str,
        creator: str,
        copyright: str,
        rating: int,
        label: str,
        custom_metadata: str,
    ) -> Dict[str, Any]:
        """Build XMP metadata dictionary."""

        xmp = {
            "xmp_version": "1.0",
            "created_date": datetime.utcnow().isoformat() + "Z",
            "tool": "ComfyUI FFpy Save with Metadata",
        }

        # Dublin Core metadata
        dc = {}
        if title:
            dc["title"] = title
        if description:
            dc["description"] = description
        if keywords:
            dc["subject"] = [k.strip() for k in keywords.split(",") if k.strip()]
        if creator:
            dc["creator"] = creator
        if copyright:
            dc["rights"] = copyright

        if dc:
            xmp["dc"] = dc

        # XMP Basic metadata
        xmp_basic = {}
        if rating > 0:
            xmp_basic["Rating"] = rating
        if label != "None":
            xmp_basic["Label"] = label

        if xmp_basic:
            xmp["xmp"] = xmp_basic

        # Custom metadata
        if custom_metadata and custom_metadata.strip():
            try:
                custom = json.loads(custom_metadata)
                xmp["custom"] = custom
            except json.JSONDecodeError:
                xmp["custom_text"] = custom_metadata

        return xmp


# Export for ComfyUI
NODE_CLASS_MAPPINGS = {
    "FFpySaveWithMetadataNode": FFpySaveWithMetadataNode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "FFpySaveWithMetadataNode": "FFpy Save with Metadata",
}
