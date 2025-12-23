# ComfyUI Metadata Nodes

Professional EXIF, XMP, and IPTC metadata workflows for ComfyUI. Works with both traditional camera images and AI-generated images.

## Overview

Three powerful custom nodes that bring professional-grade metadata capabilities to ComfyUI:

- **FFpy Add XMP to Image** - Add XMP metadata to images and save with embedded metadata (title, keywords, creator, copyright)
- **FFpy Load Image from Folder** - Load images from folders while preserving file path for metadata access
- **FFpy ExifTool (Advanced Metadata)** - Read and write 171+ metadata fields using ExifTool 13.44

## Features

### Complete Metadata Support
- **EXIF** - Camera settings, dates, GPS, exposure data
- **XMP** - Adobe metadata, Dublin Core schema (title, description, creator, copyright, keywords)
- **IPTC** - News and journalism standards
- **PNG Text Chunks** - Native PNG metadata
- **Maker Notes** - Camera-specific data
- **ICC Profiles** - Color management

### Two Display Modes
- **Verbose Mode** - Extract all metadata fields in JSON format
- **Specific Mode** - Read targeted fields in human-readable format

### Complete Workflow
- Generate or load images
- Embed custom metadata
- Save to file
- Load back from folder
- Extract and display metadata

## Installation

### Prerequisites

1. **ComfyUI** installed and working
2. **ExifTool 13.44** or later ([Download here](https://exiftool.org/))
3. Python packages (usually already in ComfyUI):
   - torch
   - PIL (Pillow)
   - numpy

### Install Metadata Nodes

```bash
cd ComfyUI/custom_nodes
git clone https://github.com/K1Green/comfyui-metadata-nodes.git
```

### Configure ExifTool Path

Edit `ffpy_exiftool_node.py` line 31:

```python
EXIFTOOL_PATH = "/usr/local/bin/exiftool"  # Update to your ExifTool path
```

Common paths:
- **macOS (Homebrew):** `/usr/local/bin/exiftool`
- **macOS (Manual):** `/Users/YOUR_USERNAME/Downloads/Image-ExifTool-13.44/exiftool`
- **Linux:** `/usr/bin/exiftool`
- **Windows:** `C:\\exiftool\\exiftool.exe`

See [INSTALLATION.md](INSTALLATION.md) for detailed instructions.

### Restart ComfyUI

```bash
# Stop ComfyUI, then restart it
```

Nodes will appear in: **Add Node → image → metadata**

## Quick Start

### Option 1: Import Pre-Built Workflow

1. Open ComfyUI in your browser
2. Drag `workflow_metadata_roundtrip.json` into ComfyUI
3. Press **Queue Prompt** (or Ctrl+Enter)
4. View results in output nodes

See [QUICK_START.md](QUICK_START.md) for detailed walkthrough.

### Option 2: Build Your Own

Follow the step-by-step guide in [BUILD_IT_YOURSELF.md](BUILD_IT_YOURSELF.md) to create the workflow from scratch.

## Included Workflow

### Metadata Roundtrip Workflow

**File:** `workflow_metadata_roundtrip.json`

A complete workflow demonstrating:
1. Generate AI image from text (requires Firefly node separately)
2. Save with custom metadata (title, keywords, creator, copyright)
3. Load image back from folder
4. Extract and display all metadata
5. Display specific metadata fields

**What You'll See:**
- Generated image
- Embedded metadata confirmation
- Complete metadata JSON (20+ fields)
- Human-readable metadata display

## Testing Results

This package was tested with two distinct image types:

### Camera Image: "Willow River"
- **Source:** Digital camera photograph
- **Metadata Found:**
  - EXIF: Camera make/model, lens, ISO, aperture, shutter speed
  - GPS: Location coordinates
  - Date/Time: Capture timestamp
  - Maker Notes: Camera-specific technical data
- **Result:** ✅ Full EXIF extraction successful

### AI Image: "Snow Tiger"
- **Source:** Adobe Firefly AI generation
- **Metadata Found:**
  - XMP: Title, description, creator, copyright
  - PNG Text: Keywords, generation prompt
  - Dublin Core: Subject tags
- **Result:** ✅ Full XMP/PNG extraction successful

**Conclusion:** Works with both traditional photography and AI-generated images.

## Node Documentation

### FFpy Add XMP to Image

Add XMP metadata to images and save to disk with embedded metadata.

**Inputs:**
- `image` - Image tensor to save
- `filename_prefix` - Prefix for saved filename
- `title` - Image title
- `description` - Image description
- `keywords` - Comma-separated keywords
- `creator` - Creator/artist name
- `copyright` - Copyright notice
- `rating` - Star rating (0-5)
- `label` - Color label
- `output_path` - Save location (empty = default)

**Outputs:**
- `file_path` - Full path to saved file
- `debug_log` - Formatted save log

### FFpy Load Image from Folder

Load images from a folder with powerful filtering and sorting.

**Inputs:**
- `folder_path` - Folder to scan
- `file_pattern` - Pattern match (e.g., `*.png`, `photo*.jpg`)
- `sort_by` - Sort method (date_modified, date_created, size, name)
- `sort_order` - ascending or descending
- `image_index` - Which image to load (0 = first/newest)
- `recursive` - Search subfolders

**Outputs:**
- `image` - Loaded image tensor
- `file_path` - Full path to file (**critical for ExifTool!**)
- `filename` - Just the filename
- `debug_log` - Load operation log
- `total_images` - Number of matching files

### FFpy ExifTool (Advanced Metadata)

Professional metadata reading/writing using ExifTool.

**Operations:**

**Read All Metadata:**
- Extracts all metadata fields
- Output: Complete JSON with 20-171+ fields
- Groups: EXIF, XMP, IPTC, PNG, ICC, etc.

**Read Specific Tags:**
- Specify tags to read (one per line)
- Example: Title, Description, Author, Copyright, Subject
- Output: Human-readable format

**Write Metadata:**
- Write/update specific metadata fields
- JSON format input
- Preserves existing metadata

## Architecture

### Why Direct File Path Access?

The nodes use **direct file path** rather than image tensor processing:

**The Problem:**
- ComfyUI passes images as PyTorch tensors (NumPy arrays)
- Tensors only contain pixel data (RGB values)
- Metadata lives in PNG/JPEG file structure, not pixels
- Converting tensor → temp file loses embedded metadata

**The Solution:**
- Save node returns `file_path` of saved file
- Load node returns `file_path` of loaded file
- ExifTool reads directly from file with metadata
- Complete metadata preservation guaranteed

**Critical Workflow Pattern:**
```
Save with Metadata → file_path → ExifTool ✅
Save with Metadata → image tensor → ExifTool ❌ (metadata lost!)
```

See [WORKFLOW_FIX.md](WORKFLOW_FIX.md) for detailed explanation.

## Use Cases

- **Photography Workflows** - Extract camera settings and shooting parameters
- **AI Art Attribution** - Embed and verify creator, copyright, generation data
- **Content Authentication** - Verify image source and provenance
- **Metadata Auditing** - Discover what metadata exists in images
- **Rights Management** - Track copyright and licensing information
- **Archival Systems** - Catalog images with complete metadata
- **Quality Control** - Validate metadata in processing pipelines

## Troubleshooting

### Nodes Not Appearing in ComfyUI?

1. Restart ComfyUI completely
2. Check console for Python errors
3. Verify files are in `ComfyUI/custom_nodes/comfyui-metadata-nodes/`
4. Look in category: **image → metadata**

### ExifTool Not Working?

1. Verify ExifTool is installed:
   ```bash
   exiftool -ver
   ```
2. Update `EXIFTOOL_PATH` in `ffpy_exiftool_node.py` line 31
3. Check ExifTool permissions (must be executable)
4. Restart ComfyUI after updating path

### No Metadata Returned?

**Critical:** ExifTool must receive `file_path` input!

❌ Wrong:
```
Load Image → image → ExifTool
(Creates temp file without metadata)
```

✅ Correct:
```
Load Image → image → ExifTool
Load Image → file_path → ExifTool
(Reads actual file with metadata)
```

See [WORKFLOW_FIX.md](WORKFLOW_FIX.md) for detailed explanation.

## File Structure

```
comfyui-metadata-nodes/
├── README.md                              # This file
├── INSTALLATION.md                        # Detailed installation guide
├── QUICK_START.md                         # 5-minute workflow guide
├── BUILD_IT_YOURSELF.md                   # Step-by-step node setup
├── WORKFLOW_FIX.md                        # Critical bug explanation
├── Read_EXIF_Workflow_Description.rtf     # Word document
├── LICENSE                                # MIT License
├── requirements.txt                       # Python dependencies
├── .gitignore                             # Git ignore rules
├── __init__.py                            # Node registration
├── ffpy_add_xmp_node.py                   # Add XMP to image
├── ffpy_load_image_folder_node.py         # Load from folder
├── ffpy_exiftool_node.py                  # ExifTool integration
└── workflow_metadata_roundtrip.json       # Demo workflow
```

## Requirements

### Python Packages
- `torch` (PyTorch) - Usually pre-installed with ComfyUI
- `PIL` (Pillow) - Usually pre-installed with ComfyUI
- `numpy` - Usually pre-installed with ComfyUI

### External Tools
- **ExifTool 13.44+** - Download from [exiftool.org](https://exiftool.org/)

### ComfyUI Compatibility
- Tested with ComfyUI (latest stable)
- Requires custom node support

## License

MIT License - see [LICENSE](LICENSE) file

## Credits

**Author:** Kevin Green
**Tool Integration:** ExifTool by Phil Harvey
**Platform:** ComfyUI

## Support

- **Issues:** [GitHub Issues](https://github.com/K1Green/comfyui-metadata-nodes/issues)
- **Documentation:** See included markdown files
- **Examples:** `workflow_metadata_roundtrip.json`

## Version History

### v1.0.0 (2025-12-22)
- Initial release
- FFpy Add XMP to Image node
- FFpy Load Image from Folder node
- FFpy ExifTool node with read/write support
- Complete metadata roundtrip workflow
- Tested with camera images (Willow River) and AI images (Snow Tiger)
- Comprehensive documentation

---

**Made for the ComfyUI community**

*Professional metadata workflows for traditional photography and AI-generated imagery*
