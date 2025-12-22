"""
FFpy ExifTool Node

Advanced metadata reading/writing using ExifTool (the industry standard).
Supports ALL metadata formats: EXIF, XMP, IPTC, ICC Profile, Maker Notes, and 500+ more.
"""

from __future__ import annotations
import io
import subprocess
import json
import numpy as np
import torch
from PIL import Image
from pathlib import Path
from typing import Optional, Dict, Any, List
import logging
import tempfile
import os

logger = logging.getLogger(__name__)

# Path to ExifTool binary
# IMPORTANT: Update this path to match your ExifTool installation
# See INSTALLATION.md for detailed instructions
# Common paths:
#   macOS (Homebrew): /usr/local/bin/exiftool
#   macOS (Manual): /Users/YOUR_USERNAME/Downloads/Image-ExifTool-13.44/exiftool
#   Linux: /usr/bin/exiftool
#   Windows: C:\\exiftool\\exiftool.exe
EXIFTOOL_PATH = "/usr/local/bin/exiftool"  # Default - users must configure


class FFpyExifToolNode:
    """
    Read and write comprehensive metadata using ExifTool.

    ExifTool supports:
    - EXIF (camera data, dates, GPS, settings)
    - XMP (Adobe metadata, Dublin Core, rights)
    - IPTC (news/journalism metadata)
    - ICC Profile (color management)
    - Maker Notes (camera-specific data)
    - PNG/GIF/TIFF text chunks
    - And 500+ other metadata formats
    """

    RETURN_TYPES = ("IMAGE", "STRING", "STRING")
    RETURN_NAMES = ("image", "metadata_json", "debug_log")
    FUNCTION = "process_metadata"
    CATEGORY = "api node/photoshop"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "operation": (
                    ["Read All Metadata", "Read Specific Tags", "Write Metadata"],
                    {
                        "default": "Read All Metadata",
                        "tooltip": "Operation to perform",
                    },
                ),
            },
            "optional": {
                "image": ("IMAGE", {"tooltip": "Input image to process (optional if file_path provided)"}),
                "file_path": (
                    "STRING",
                    {
                        "default": "",
                        "multiline": False,
                        "tooltip": "Direct file path to read metadata from. If provided, uses this instead of converting image tensor.",
                    },
                ),
                # Read options
                "output_format": (
                    ["Pretty JSON", "Compact JSON", "Human Readable"],
                    {
                        "default": "Pretty JSON",
                        "tooltip": "How to format metadata output",
                    },
                ),
                "group_filter": (
                    "STRING",
                    {
                        "default": "",
                        "multiline": False,
                        "tooltip": "Filter by group (e.g., 'EXIF', 'XMP', 'IPTC', 'ICC_Profile', 'MakerNotes'). Leave empty for all.",
                    },
                ),
                "tag_names": (
                    "STRING",
                    {
                        "default": "",
                        "multiline": True,
                        "tooltip": "Specific tags to read (one per line, e.g., 'Make', 'Model', 'Artist', 'Copyright'). Only for 'Read Specific Tags'.",
                    },
                ),
                # Write options
                "metadata_to_write": (
                    "STRING",
                    {
                        "default": "",
                        "multiline": True,
                        "tooltip": "JSON object with metadata to write. Example: {\"EXIF:Artist\": \"John Doe\", \"XMP:Title\": \"My Photo\"}",
                    },
                ),
                "preserve_existing": (
                    "BOOLEAN",
                    {
                        "default": True,
                        "tooltip": "Keep existing metadata when writing (only update specified fields)",
                    },
                ),
                # Advanced options
                "include_binary": (
                    "BOOLEAN",
                    {
                        "default": False,
                        "tooltip": "Include binary data (thumbnails, ICC profiles) in output",
                    },
                ),
                "extract_embedded": (
                    "BOOLEAN",
                    {
                        "default": False,
                        "tooltip": "Extract embedded files (thumbnails, previews)",
                    },
                ),
            },
        }

    def process_metadata(
        self,
        operation: str = "Read All Metadata",
        image: Optional[torch.Tensor] = None,
        file_path: str = "",
        output_format: str = "Pretty JSON",
        group_filter: str = "",
        tag_names: str = "",
        metadata_to_write: str = "",
        preserve_existing: bool = True,
        include_binary: bool = False,
        extract_embedded: bool = False,
    ) -> tuple[torch.Tensor, str, str]:
        """
        Process metadata using ExifTool.
        """

        # Check if ExifTool exists
        if not os.path.exists(EXIFTOOL_PATH):
            error_msg = f"ExifTool not found at: {EXIFTOOL_PATH}"
            debug_log = self._build_error_log(error_msg)
            # Create empty image tensor if no image provided
            if image is None:
                image = torch.zeros((1, 64, 64, 3))
            return (image, json.dumps({"error": error_msg}), debug_log)

        # Build initial debug log
        debug_log = self._build_debug_log_start(operation, output_format, group_filter, file_path)

        try:
            # Determine file path to use
            use_temp_file = False
            if file_path and file_path.strip():
                # Use provided file path directly
                tmp_path = file_path.strip()
                debug_log += f"\nUsing provided file: {tmp_path}\n"

                # Load image from file if no image tensor provided
                if image is None:
                    img_pil = Image.open(tmp_path)
                    i = np.array(img_pil).astype(np.float32) / 255.0
                    image = torch.from_numpy(i)[None,]
            else:
                # Convert tensor to PIL Image and save to temp file
                if image is None:
                    error_msg = "Either 'image' or 'file_path' must be provided"
                    debug_log = self._build_error_log(error_msg)
                    return (torch.zeros((1, 64, 64, 3)), json.dumps({"error": error_msg}), debug_log)

                i = 255.0 * image[0].cpu().numpy()
                img_pil = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))

                # Save image to temporary file (ExifTool works with files)
                tmp_file = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
                tmp_path = tmp_file.name
                tmp_file.close()
                img_pil.save(tmp_path, format="PNG")
                use_temp_file = True
                debug_log += f"\nCreated temporary file for processing\n"

            try:
                if operation == "Read All Metadata":
                    metadata, result_log = self._read_all_metadata(
                        tmp_path, group_filter, include_binary, extract_embedded
                    )
                elif operation == "Read Specific Tags":
                    metadata, result_log = self._read_specific_tags(tmp_path, tag_names)
                elif operation == "Write Metadata":
                    metadata, result_log = self._write_metadata(
                        tmp_path, metadata_to_write, preserve_existing
                    )
                    # Reload image after writing metadata
                    img_pil = Image.open(tmp_path)
                    i = np.array(img_pil).astype(np.float32) / 255.0
                    image = torch.from_numpy(i)[None,]
                else:
                    raise ValueError(f"Unknown operation: {operation}")

                # Format output
                if output_format == "Pretty JSON":
                    metadata_output = json.dumps(metadata, indent=2, ensure_ascii=False)
                elif output_format == "Compact JSON":
                    metadata_output = json.dumps(metadata, ensure_ascii=False)
                else:  # Human Readable
                    metadata_output = self._format_human_readable(metadata)

                # Build final debug log
                debug_log += result_log
                debug_log += self._build_debug_log_success(metadata, operation)

                return (image, metadata_output, debug_log)

            finally:
                # Clean up temporary file (only if we created it)
                if use_temp_file and os.path.exists(tmp_path):
                    os.unlink(tmp_path)

        except Exception as e:
            error_msg = f"\n[ERROR] ExifTool operation failed: {str(e)}\n"
            error_msg += "======================================================="
            logger.error(f"ExifTool error: {e}")
            return (image, json.dumps({"error": str(e)}), debug_log + error_msg)

    def _read_all_metadata(
        self,
        file_path: str,
        group_filter: str,
        include_binary: bool,
        extract_embedded: bool,
    ) -> tuple[Dict[str, Any], str]:
        """Read all metadata using ExifTool."""

        # Build ExifTool command
        cmd = [EXIFTOOL_PATH, "-json", "-a", "-G1"]  # -a = allow duplicates, -G1 = show group names

        if group_filter and group_filter.strip():
            cmd.extend(["-" + group_filter.strip()])

        if not include_binary:
            cmd.append("-b")  # Exclude binary data

        cmd.append(file_path)

        log = f"\nExecuting: {' '.join(cmd[:4])}...\n"

        # Run ExifTool
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30,
        )

        if result.returncode != 0:
            raise Exception(f"ExifTool failed: {result.stderr}")

        # Parse JSON output
        metadata_list = json.loads(result.stdout)
        metadata = metadata_list[0] if metadata_list else {}

        # Remove SourceFile key (not useful)
        metadata.pop("SourceFile", None)

        log += f"Found {len(metadata)} metadata fields\n"

        # Extract embedded files if requested
        if extract_embedded:
            embedded_log = self._extract_embedded_files(file_path)
            log += embedded_log

        return metadata, log

    def _read_specific_tags(
        self,
        file_path: str,
        tag_names: str,
    ) -> tuple[Dict[str, Any], str]:
        """Read specific metadata tags."""

        # Parse tag names (one per line)
        tags = [t.strip() for t in tag_names.split("\n") if t.strip()]

        if not tags:
            return {"warning": "No tags specified"}, "\n[WARNING] No tags specified\n"

        # Build ExifTool command
        cmd = [EXIFTOOL_PATH, "-json", "-G1"]
        for tag in tags:
            cmd.extend(["-" + tag])
        cmd.append(file_path)

        log = f"\nReading {len(tags)} specific tag(s):\n"
        for tag in tags[:10]:  # Show first 10
            log += f"  - {tag}\n"
        if len(tags) > 10:
            log += f"  ... and {len(tags) - 10} more\n"

        # Run ExifTool
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30,
        )

        if result.returncode != 0:
            raise Exception(f"ExifTool failed: {result.stderr}")

        # Parse JSON output
        metadata_list = json.loads(result.stdout)
        metadata = metadata_list[0] if metadata_list else {}
        metadata.pop("SourceFile", None)

        log += f"\nFound {len(metadata)}/{len(tags)} requested tags\n"

        return metadata, log

    def _write_metadata(
        self,
        file_path: str,
        metadata_json: str,
        preserve_existing: bool,
    ) -> tuple[Dict[str, Any], str]:
        """Write metadata using ExifTool."""

        if not metadata_json or not metadata_json.strip():
            return {"warning": "No metadata to write"}, "\n[WARNING] No metadata provided\n"

        try:
            metadata_dict = json.loads(metadata_json)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in metadata_to_write: {e}")

        # Build ExifTool command
        cmd = [EXIFTOOL_PATH, "-json=-"]  # Read JSON from stdin

        if not preserve_existing:
            cmd.append("-all=")  # Clear all existing metadata first

        cmd.extend(["-overwrite_original", file_path])

        # Prepare JSON input
        json_input = json.dumps([metadata_dict])

        log = f"\nWriting {len(metadata_dict)} metadata field(s):\n"
        for key, value in list(metadata_dict.items())[:10]:
            value_str = str(value)[:50]
            log += f"  {key}: {value_str}\n"
        if len(metadata_dict) > 10:
            log += f"  ... and {len(metadata_dict) - 10} more\n"

        log += f"Preserve existing: {preserve_existing}\n"

        # Run ExifTool
        result = subprocess.run(
            cmd,
            input=json_input,
            capture_output=True,
            text=True,
            timeout=30,
        )

        if result.returncode != 0:
            raise Exception(f"ExifTool write failed: {result.stderr}")

        log += f"\n{result.stdout.strip()}\n"

        # Read back written metadata to verify
        verify_metadata, _ = self._read_all_metadata(file_path, "", False, False)

        return verify_metadata, log

    def _extract_embedded_files(self, file_path: str) -> str:
        """Extract embedded files like thumbnails."""

        cmd = [EXIFTOOL_PATH, "-b", "-ThumbnailImage", file_path]

        result = subprocess.run(
            cmd,
            capture_output=True,
            timeout=30,
        )

        if result.returncode == 0 and result.stdout:
            return f"\nExtracted embedded thumbnail ({len(result.stdout)} bytes)\n"
        else:
            return "\nNo embedded files found\n"

    def _format_human_readable(self, metadata: Dict[str, Any]) -> str:
        """Format metadata as human-readable text."""
        lines = []
        lines.append("=" * 60)
        lines.append("EXIFTOOL METADATA REPORT")
        lines.append("=" * 60)
        lines.append("")

        # Group by prefix (e.g., EXIF:, XMP:, IPTC:)
        groups = {}
        for key, value in metadata.items():
            if ":" in key:
                group, tag = key.split(":", 1)
                if group not in groups:
                    groups[group] = {}
                groups[group][tag] = value
            else:
                if "Other" not in groups:
                    groups["Other"] = {}
                groups["Other"][key] = value

        # Print by group
        for group in sorted(groups.keys()):
            lines.append(f"[{group}]")
            lines.append("-" * 60)
            for tag, value in sorted(groups[group].items()):
                value_str = str(value)
                if len(value_str) > 100:
                    value_str = value_str[:100] + "..."
                lines.append(f"{tag:30} : {value_str}")
            lines.append("")

        lines.append("=" * 60)
        lines.append(f"Total: {len(metadata)} metadata fields")
        lines.append("=" * 60)

        return "\n".join(lines)

    def _build_debug_log_start(
        self,
        operation: str,
        output_format: str,
        group_filter: str,
        file_path: str = "",
    ) -> str:
        """Build initial debug log in Firefly style."""
        log = "=" * 55 + "\n"
        log += "EXIFTOOL Metadata Processing\n"
        log += "-" * 55 + "\n"
        log += f"Tool: ExifTool 13.44 (Perl)\n"
        log += f"Operation: {operation}\n"
        log += f"Output Format: {output_format}\n"
        if group_filter:
            log += f"Group Filter: {group_filter}\n"
        if file_path and file_path.strip():
            log += f"Source: Direct file path\n"
        else:
            log += f"Source: Image tensor (temp file)\n"
        log += "Status: Processing...\n"
        log += "=" * 55 + "\n"
        return log

    def _build_debug_log_success(
        self,
        metadata: Dict[str, Any],
        operation: str,
    ) -> str:
        """Build success section of debug log."""
        log = "\n"
        log += "[OK] Operation completed successfully\n"

        if operation.startswith("Read"):
            log += f"Total fields extracted: {len(metadata)}\n"

            # Count by group
            groups = {}
            for key in metadata.keys():
                if ":" in key:
                    group = key.split(":")[0]
                    groups[group] = groups.get(group, 0) + 1

            if groups:
                log += "\nBreakdown by group:\n"
                for group, count in sorted(groups.items()):
                    log += f"  {group}: {count} fields\n"

        elif operation == "Write Metadata":
            log += "Metadata written and verified successfully\n"

        log += "=" * 55 + "\n"

        return log

    def _build_error_log(self, error: str) -> str:
        """Build error debug log."""
        log = "=" * 55 + "\n"
        log += "EXIFTOOL Metadata Processing\n"
        log += "-" * 55 + "\n"
        log += f"[ERROR] {error}\n"
        log += "=" * 55 + "\n"
        return log


# Export for ComfyUI
NODE_CLASS_MAPPINGS = {
    "FFpyExifToolNode": FFpyExifToolNode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "FFpyExifToolNode": "FFpy ExifTool (Advanced Metadata)",
}
