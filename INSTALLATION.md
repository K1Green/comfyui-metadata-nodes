# Installation Guide - FFpy Metadata Nodes

Complete installation instructions for FFpy Metadata Nodes for ComfyUI.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Install ExifTool](#install-exiftool)
3. [Install FFpy Nodes](#install-ffpy-nodes)
4. [Configure ExifTool Path](#configure-exiftool-path)
5. [Verify Installation](#verify-installation)
6. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### 1. ComfyUI Installed

You must have ComfyUI installed and working. If not, install it first:

```bash
git clone https://github.com/comfyanonymous/ComfyUI.git
cd ComfyUI
pip install -r requirements.txt
```

### 2. Python Environment

ComfyUI's Python environment should already have:
- Python 3.8+
- PyTorch
- Pillow (PIL)
- NumPy

No additional Python packages are required.

---

## Install ExifTool

ExifTool is **required** for the FFpy ExifTool node to function.

### macOS

**Option 1: Download Pre-Built Binary**

1. Visit [https://exiftool.org/](https://exiftool.org/)
2. Download **MacOS Package**
3. Extract the archive:
   ```bash
   cd ~/Downloads
   tar -xzf Image-ExifTool-13.44.tar.gz
   ```
4. Note the path: `/Users/YOUR_USERNAME/Downloads/Image-ExifTool-13.44/exiftool`

**Option 2: Homebrew**

```bash
brew install exiftool
which exiftool  # Note this path
```

### Linux

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install libimage-exiftool-perl
which exiftool  # Note this path
```

**Fedora/RHEL:**
```bash
sudo dnf install perl-Image-ExifTool
which exiftool  # Note this path
```

**From Source:**
```bash
cd ~/Downloads
wget https://exiftool.org/Image-ExifTool-13.44.tar.gz
tar -xzf Image-ExifTool-13.44.tar.gz
cd Image-ExifTool-13.44
perl Makefile.PL
make test
sudo make install
```

### Windows

1. Visit [https://exiftool.org/](https://exiftool.org/)
2. Download **Windows Executable**
3. Extract `exiftool(-k).exe` to a folder (e.g., `C:\exiftool\`)
4. Rename to `exiftool.exe`
5. Note the path: `C:\exiftool\exiftool.exe`

**Verify Installation:**
```bash
exiftool -ver
# Should show: 13.44 (or your version)
```

---

## Install FFpy Nodes

### Method 1: Git Clone (Recommended)

```bash
# Navigate to ComfyUI custom_nodes directory
cd /path/to/ComfyUI/custom_nodes

# Clone this repository
git clone https://github.com/K1Green/firefly_services_nodes.git

# Verify files
ls firefly_services_nodes/
```

### Method 2: Download ZIP

1. Download ZIP from GitHub
2. Extract to `ComfyUI/custom_nodes/firefly_services_nodes/`
3. Verify folder structure matches:
   ```
   ComfyUI/
   └── custom_nodes/
       └── firefly_services_nodes/
           ├── README.md
           ├── Photoshop/
           │   ├── __init__.py
           │   ├── ffpy_save_with_metadata_node.py
           │   ├── ffpy_load_image_folder_node.py
           │   └── ffpy_exiftool_node.py
           └── workflow_metadata_roundtrip.json
   ```

---

## Configure ExifTool Path

**CRITICAL:** You must configure the ExifTool path for the node to work.

### 1. Find Your ExifTool Path

**macOS/Linux:**
```bash
which exiftool
# Or if you downloaded it:
# /Users/YOUR_USERNAME/Downloads/Image-ExifTool-13.44/exiftool
```

**Windows:**
```
C:\exiftool\exiftool.exe
```

### 2. Edit the Node File

Open this file in a text editor:
```
ComfyUI/custom_nodes/firefly_services_nodes/Photoshop/ffpy_exiftool_node.py
```

Find line 24:
```python
EXIFTOOL_PATH = "/Users/kevin/Downloads/Image-ExifTool-13.44/exiftool"
```

Change it to your ExifTool path:

**macOS/Linux Example:**
```python
EXIFTOOL_PATH = "/usr/local/bin/exiftool"
# or
EXIFTOOL_PATH = "/Users/YOUR_USERNAME/Downloads/Image-ExifTool-13.44/exiftool"
```

**Windows Example:**
```python
EXIFTOOL_PATH = "C:\\exiftool\\exiftool.exe"
# Note: Use double backslashes or forward slashes
```

Save the file.

---

## Verify Installation

### 1. Restart ComfyUI

**IMPORTANT:** ComfyUI must be restarted to load the new nodes.

```bash
# Stop ComfyUI (Ctrl+C in terminal)
# Then start it again
python main.py
# or
python3 main.py --listen 0.0.0.0
```

### 2. Check Console Output

Look for messages like:
```
Loading: /path/to/ComfyUI/custom_nodes/firefly_services_nodes
Imported: firefly_services_nodes
```

**No errors = success!**

### 3. Find Nodes in ComfyUI

1. Open ComfyUI in browser: `http://localhost:8188`
2. Right-click on canvas
3. Navigate to: **Add Node → api node → photoshop**
4. You should see:
   - FFpy Save with Metadata
   - FFpy Load Image from Folder
   - FFpy ExifTool (Advanced Metadata)

### 4. Test the Workflow

1. **Drag** `workflow_metadata_roundtrip.json` into ComfyUI
2. **Press** Queue Prompt (or Ctrl+Enter)
3. **Wait** ~10 seconds for processing
4. **Check** Node 13 for metadata output

**Success looks like:**
```
============================================================
EXIFTOOL METADATA REPORT
============================================================

[PNG]
------------------------------------------------------------
Title                          : AI Snow Leopard
Author                         : Kevin Green
Copyright                      : 2025

[XMP-dc]
------------------------------------------------------------
Subject                        : AI, Firefly, Wildlife
```

---

## Troubleshooting

### Nodes Not Showing in ComfyUI

**Problem:** Can't find FFpy nodes in "Add Node" menu

**Solutions:**
1. Verify folder structure:
   ```bash
   ls ComfyUI/custom_nodes/firefly_services_nodes/Photoshop/
   # Should show __init__.py and three node files
   ```

2. Check ComfyUI console for errors:
   ```
   Error loading node pack: firefly_services_nodes
   ```

3. Restart ComfyUI completely (kill process, restart)

4. Look in different category - try:
   - `api node/photoshop`
   - `api node/firefly`
   - Search for "FFpy"

### ExifTool Errors

**Problem:** "ExifTool not found at: /path/to/exiftool"

**Solutions:**
1. Verify ExifTool is installed:
   ```bash
   exiftool -ver
   ```

2. Find correct path:
   ```bash
   which exiftool  # macOS/Linux
   where exiftool  # Windows
   ```

3. Update `EXIFTOOL_PATH` in `ffpy_exiftool_node.py` line 24

4. Make ExifTool executable (macOS/Linux):
   ```bash
   chmod +x /path/to/exiftool
   ```

5. Restart ComfyUI after updating path

### No Metadata Returned

**Problem:** ExifTool runs but shows "No metadata found"

**Solution:** Ensure `file_path` is connected!

**Wrong Connection:**
```
Load Image → image → ExifTool
```

**Correct Connection:**
```
Load Image → image → ExifTool
Load Image → file_path → ExifTool  ← CRITICAL!
```

See [WORKFLOW_FIX.md](WORKFLOW_FIX.md) for detailed explanation.

### Python Import Errors

**Problem:** "ModuleNotFoundError: No module named 'torch'"

**Solutions:**
1. Make sure you're using ComfyUI's Python environment
2. Install missing packages:
   ```bash
   pip install torch pillow numpy
   ```

### Permission Errors

**Problem:** "Permission denied" when saving files

**Solutions:**
1. Check output folder permissions:
   ```bash
   ls -la ComfyUI/output/
   ```

2. Create output folder if missing:
   ```bash
   mkdir -p ComfyUI/output
   ```

3. Fix permissions:
   ```bash
   chmod 755 ComfyUI/output
   ```

### Workflow Import Fails

**Problem:** Can't import `workflow_metadata_roundtrip.json`

**Solutions:**
1. Verify JSON is valid:
   ```bash
   cat workflow_metadata_roundtrip.json | python -m json.tool
   ```

2. Try drag-and-drop instead of menu import

3. Check console for specific error messages

---

## Optional Dependencies

### ComfyUI-Custom-Scripts (for ShowText node)

The example workflow uses `ShowText|pysssss` node. If you don't have it:

```bash
cd ComfyUI/custom_nodes
git clone https://github.com/pythongosssss/ComfyUI-Custom-Scripts
```

**Alternative:** Use built-in `SaveText` node instead.

---

## Platform-Specific Notes

### macOS

- **Apple Silicon (M1/M2):** Works perfectly with native PyTorch
- **Intel:** Works with standard PyTorch installation
- **ExifTool:** Perl is built-in, ExifTool works natively

### Linux

- **Ubuntu 20.04+:** Fully tested and working
- **Debian/Fedora:** Should work identically
- **ExifTool:** Install via package manager or from source

### Windows

- **ExifTool:** Use `.exe` version, not Perl version
- **Paths:** Use `\\` or `/` in Python strings
- **WSL:** ExifTool works in WSL with Linux installation

---

## Uninstallation

To remove FFpy Metadata Nodes:

```bash
# Remove the folder
rm -rf ComfyUI/custom_nodes/firefly_services_nodes

# Restart ComfyUI
```

Nodes will no longer appear in the menu.

---

## Next Steps

After successful installation:

1. **Quick Start:** See [QUICK_START.md](QUICK_START.md)
2. **Build Your Own:** See [BUILD_IT_YOURSELF.md](BUILD_IT_YOURSELF.md)
3. **Documentation:** See [README.md](README.md)
4. **Examples:** Try `workflow_metadata_roundtrip.json`

---

## Support

- **Issues:** Report bugs on GitHub Issues
- **Questions:** Check existing documentation first
- **Contributions:** Pull requests welcome!

---

**Installation complete!** 🎉

You can now use professional metadata workflows in ComfyUI.
