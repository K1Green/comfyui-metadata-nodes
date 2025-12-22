# GitHub Release Announcement Template

Use this template when creating a release on GitHub.

---

## Creating the Release on GitHub

1. Go to your repository: https://github.com/K1Green/comfyui-metadata-nodes
2. Click **Releases** → **Create a new release**
3. Click **"Choose a tag"** → Type: `v1.0.0` → Click **"Create new tag: v1.0.0 on publish"**
4. **Release title:** `Professional Metadata Workflows for ComfyUI v1.0.0`
5. **Description:** Copy the text below
6. **Attach files:** Upload `workflow_metadata_roundtrip.json` as a binary attachment
7. Click **Publish release**

---

## Release Description (Copy & Paste This)

```markdown
# Professional Metadata Workflows for ComfyUI v1.0.0

🎉 **Initial Release** - Complete EXIF, XMP, and IPTC metadata support for ComfyUI!

## 🎯 What This Package Does

Extract, embed, and manage professional metadata in your ComfyUI workflows. Works with both traditional camera images and AI-generated images.

## ✨ Features

### Three Powerful Nodes

1. **FFpy Save with Metadata**
   - Embed XMP metadata directly into images
   - Fields: Title, Description, Keywords, Creator, Copyright, Rating, Label
   - Save to custom folders or default output

2. **FFpy Load Image from Folder**
   - Load images from folders with pattern matching
   - Sort by date, size, or name
   - Preserves file path for metadata access
   - Returns filename and total image count

3. **FFpy ExifTool (Advanced Metadata)**
   - Read/write 171+ metadata fields
   - Supports: EXIF, XMP, IPTC, PNG text, ICC profiles, Maker notes
   - Three modes: Read All, Read Specific Tags, Write Metadata
   - Human-readable or JSON output

### Complete Workflow Included

📦 **`workflow_metadata_roundtrip.json`** - Demonstrates full metadata lifecycle:
1. Generate image (or load existing)
2. Save with custom metadata
3. Load back from folder
4. Extract all metadata
5. Display specific fields

## 🚀 Quick Start

### Installation

```bash
cd ComfyUI/custom_nodes
git clone https://github.com/K1Green/comfyui-metadata-nodes.git
```

### Configure ExifTool

1. Download ExifTool from https://exiftool.org/
2. Edit `ffpy_exiftool_node.py` line 31 with your ExifTool path
3. Restart ComfyUI

### Run the Workflow

1. Import `workflow_metadata_roundtrip.json` into ComfyUI
2. Press **Queue Prompt**
3. View metadata in output nodes!

See **[QUICK_START.md](QUICK_START.md)** for detailed 5-minute guide.

## ✅ Tested With

### Camera Image: Willow River
- ✅ Full EXIF extraction (camera, lens, settings, GPS)
- ✅ Maker notes and technical data
- ✅ Date/time information

### AI Image: Snow Tiger
- ✅ XMP metadata (title, description, creator, copyright)
- ✅ PNG text chunks (keywords, generation prompt)
- ✅ Dublin Core schema

**Result:** Works perfectly with both traditional photography and AI-generated images.

## 📚 Documentation

- **[README.md](README.md)** - Complete package documentation
- **[INSTALLATION.md](INSTALLATION.md)** - Detailed installation guide
- **[QUICK_START.md](QUICK_START.md)** - 5-minute tutorial
- **[BUILD_IT_YOURSELF.md](BUILD_IT_YOURSELF.md)** - Step-by-step manual build
- **[WORKFLOW_FIX.md](WORKFLOW_FIX.md)** - Technical architecture explanation
- **Read_EXIF_Workflow_Description.rtf** - Word document overview

## 🎨 Use Cases

- **Photography Workflows** - Extract camera settings and shooting parameters
- **AI Art Attribution** - Embed creator, copyright, and generation metadata
- **Content Authentication** - Verify image source and provenance
- **Rights Management** - Track copyright and licensing information
- **Archival Systems** - Catalog images with complete metadata
- **Quality Control** - Validate metadata in processing pipelines

## 🔧 Technical Highlights

### Direct File Path Architecture

Unlike tensor-based approaches, these nodes use **direct file path access** to preserve metadata:

- Image tensors only contain pixel data (RGB values)
- Metadata lives in file structure (PNG chunks, JPEG segments)
- Nodes pass `file_path` directly to ExifTool
- **Result:** Zero metadata loss

### Metadata Support

**Read Operations:**
- EXIF groups: Image, Camera, GPS, Thumbnail, MakerNotes
- XMP namespaces: dc, xmp, xmpRights, photoshop, Iptc4xmpCore
- IPTC fields: All standard IPTC/IIM fields
- PNG: tEXt, iTXt, zTXt chunks
- Total: 171+ metadata fields

**Write Operations:**
- Preserve existing metadata while updating specific fields
- JSON-based metadata input
- Supports all ExifTool-writable formats

## 📦 What's Included

- 3 custom nodes for ComfyUI
- 1 complete demo workflow
- 6 documentation files
- MIT License
- Clean, minimal dependencies

## 💻 Compatibility

- **Platforms:** macOS, Linux, Windows
- **ComfyUI:** Latest stable version
- **Python:** 3.8+ (via ComfyUI)
- **Dependencies:** torch, Pillow, numpy (usually pre-installed)
- **External:** ExifTool 13.44+ required

## 🐛 Known Issues

None - workflow tested and validated with multiple image types.

## 🙏 Credits

- **Author:** Kevin Green
- **ExifTool:** Phil Harvey (https://exiftool.org/)
- **Platform:** ComfyUI
- **License:** MIT

## 📝 Changelog

### v1.0.0 (2025-12-22)

**Initial Release**

- FFpy Save with Metadata node
- FFpy Load Image from Folder node
- FFpy ExifTool (Advanced Metadata) node
- Complete metadata roundtrip workflow
- Comprehensive documentation
- Tested with camera images and AI-generated images

## 🔗 Links

- **Repository:** https://github.com/K1Green/comfyui-metadata-nodes
- **Issues:** https://github.com/K1Green/comfyui-metadata-nodes/issues
- **ExifTool:** https://exiftool.org/

## 📄 License

MIT License - Free to use, modify, and distribute.

---

**Ready to use!** Import the workflow and start managing metadata professionally in ComfyUI.

If you encounter any issues, please [open an issue](https://github.com/K1Green/comfyui-metadata-nodes/issues).

Happy metadata management! 🎉
```

---

## Social Media Announcement Templates

### Discord (ComfyUI Server)

```
🎉 New Release: ComfyUI Metadata Nodes v1.0.0

Professional EXIF, XMP, and IPTC metadata workflows for ComfyUI!

✨ Features:
• Save images with custom metadata (title, keywords, creator, copyright)
• Load images from folders with pattern matching
• Extract 171+ metadata fields with ExifTool
• Works with camera images AND AI-generated images

📦 Installation:
cd ComfyUI/custom_nodes
git clone https://github.com/K1Green/comfyui-metadata-nodes.git

🔗 https://github.com/K1Green/comfyui-metadata-nodes

Includes complete demo workflow! ✨
```

### Reddit (r/comfyui)

**Title:** `[Release] ComfyUI Metadata Nodes v1.0.0 - Professional EXIF/XMP/IPTC Support`

**Post:**
```
I've created a set of metadata nodes for ComfyUI that let you embed and extract professional metadata from images.

**What it does:**
- Embed XMP metadata (title, keywords, creator, copyright) when saving images
- Load images from folders with smart filtering and sorting
- Extract EXIF, XMP, IPTC metadata using ExifTool (171+ fields)
- Works with both camera photos and AI-generated images

**Tested with:**
- Camera images (full EXIF extraction - settings, GPS, etc.)
- AI images from Firefly (XMP metadata, PNG text chunks)

**Installation:**
```bash
cd ComfyUI/custom_nodes
git clone https://github.com/K1Green/comfyui-metadata-nodes.git
```

**Includes:**
- 3 custom nodes
- Complete demo workflow
- Detailed documentation

Repository: https://github.com/K1Green/comfyui-metadata-nodes

Let me know if you have questions!
```

### Twitter/X

**Tweet 1:**
```
🎉 Released: ComfyUI Metadata Nodes v1.0.0

Professional EXIF/XMP/IPTC metadata support for @ComfyUI

✨ Embed metadata (title, creator, copyright)
✨ Extract 171+ metadata fields
✨ Works with camera & AI images

https://github.com/K1Green/comfyui-metadata-nodes

#ComfyUI #AI #Metadata #OpenSource
```

**Tweet 2 (Thread):**
```
Ever wanted to add proper metadata to your AI-generated images in ComfyUI?

New package lets you:
• Embed creator info & copyright
• Extract EXIF/XMP data
• Manage metadata like a pro

Works with camera photos AND AI images!

🔗 https://github.com/K1Green/comfyui-metadata-nodes

#ComfyUI #AIArt
```

---

## After Publishing Checklist

After creating the release:

- [ ] Announce on ComfyUI Discord (#custom-nodes channel)
- [ ] Post on r/comfyui
- [ ] Tweet/post on X with #ComfyUI hashtag
- [ ] Add "Topics" to GitHub repo: comfyui, metadata, exif, xmp, python, image-processing
- [ ] Enable GitHub Issues for user feedback
- [ ] Consider adding to ComfyUI Manager registry (optional)
- [ ] Star your own repo (why not! 😄)

---

## Support & Maintenance

**Monitor:**
- GitHub Issues for bug reports
- GitHub Discussions for questions
- Pull requests for contributions

**Respond to:**
- Installation problems
- ExifTool configuration issues
- Metadata extraction questions
- Feature requests

---

**Ready to announce! 🚀**

The metadata nodes are ready for the ComfyUI community!
