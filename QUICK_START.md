# Quick Start - Metadata Roundtrip Workflow

## 🚀 5-Minute Setup

### Step 1: Import Workflow

1. **Restart ComfyUI** (to load new FFpy nodes)
2. Open ComfyUI in your browser
3. **Drag and drop** this file into ComfyUI:
   ```
   workflow_metadata_roundtrip.json
   ```
4. Workflow loads automatically!

### Step 2: Run It!

1. **Press** "Queue Prompt" (or Ctrl+Enter)
2. **Wait** for Firefly to generate the snow leopard (~10 seconds)
3. **Done!** All nodes execute automatically

### Step 3: View Results

Check these nodes in order:

| Node # | Title | What You See |
|--------|-------|--------------|
| **2** | Preview Generated | AI snow leopard image |
| **4** | Save Debug Log | "✅ 7 metadata fields saved" |
| **6** | Preview Loaded | Same image (loaded from file) |
| **8** | Filename | "AI_Snow_Leopard_*.png" |
| **13** | **YOUR METADATA** | **Title, Keywords, Creator, Copyright** |

### Expected Output (Node 13)

```
============================================================
EXIFTOOL METADATA REPORT
============================================================

[PNG]
------------------------------------------------------------
Title                          : AI Snow Leopard
Description                    : majestic photorealistic snow leopard...
Author                         : Kevin Green
Copyright                      : 2025

[XMP-dc]
------------------------------------------------------------
Subject                        : AI, Firefly, Wildlife

============================================================
```

## ✅ Success Checklist

After running, you should see:

- ✅ Two identical images (Nodes 2 & 6)
- ✅ "Image saved successfully" in Node 4
- ✅ Your metadata in Node 13:
  - Title: AI Snow Leopard
  - Keywords: AI, Firefly, Wildlife
  - Creator: Kevin Green
  - Copyright: 2025

## 🎨 Customize It

### Change the Image

**Edit Node 1:**
```
prompt: "majestic eagle soaring over mountains"
```

### Change YOUR Metadata

**Edit Node 3:**
```
title: "My AI Eagle"
keywords: "AI, Bird, Nature"
creator: "YOUR NAME HERE"
copyright: "2025 YOUR NAME"
```

### Change Output Folder

**Edit Node 3:**
```
output_path: "/Users/kevin/Pictures/My_AI_Art"
```

**Edit Node 5:**
```
folder_path: "/Users/kevin/Pictures/My_AI_Art"
```

## 🔧 Troubleshooting

### Nodes Missing?

1. Restart ComfyUI
2. Look in category: `api node/photoshop`
3. You should see:
   - FFpy Save with Metadata
   - FFpy Load Image from Folder
   - FFpy ExifTool (Advanced Metadata)

### ExifTool Error?

**Fix:** Update the path in `ffpy_exiftool_node.py`:
```python
EXIFTOOL_PATH = "/Users/kevin/Downloads/Image-ExifTool-13.44/exiftool"
```

### Load Doesn't Find File?

**Wait** 1-2 seconds after save, then try:
- Press F5 to refresh
- Or queue prompt again

### No Metadata Shown?

1. Check Node 4 - Did save succeed?
2. Check Node 10 - See full JSON metadata
3. Verify ExifTool is working

## 📊 What This Workflow Does

```
1. Generate Image    → Firefly creates snow leopard
2. Save + Metadata   → Embeds title, keywords, creator, copyright
3. Load from Folder  → Reads file back
4. Extract Metadata  → ExifTool reads all fields
5. Display Results   → Shows YOUR metadata!
```

**Complete cycle in one workflow!** ✨

## 🎯 Key Nodes Explained

### Node 1: Firefly Text to Image
Generates the AI image

### Node 3: FFpy Save with Metadata ⭐
**THIS IS WHERE METADATA IS SAVED!**
- Embeds all metadata into PNG file
- Returns file_path for next node

### Node 5: FFpy Load Image from Folder ⭐
**THIS LOADS THE FILE BACK!**
- Scans folder for AI_Snow_Leopard*.png
- Loads newest file (index 0)
- Returns file_path to ExifTool

### Node 9: ExifTool Read All
Reads ALL metadata (20+ fields)

### Node 12: ExifTool Read Specific ⭐
**THIS SHOWS YOUR METADATA!**
- Reads only Title, Description, Author, Copyright, Subject
- Displays in human-readable format

## 💡 Pro Tips

1. **Check Node 4 first** - Confirms save worked
2. **Node 13 is the payoff** - Your metadata displayed!
3. **Connect Show Text nodes** to debug_log outputs for details
4. **File path matters** - ExifTool reads from original file, not tensor

## 🎉 You Did It!

You just:
- ✅ Generated an AI image
- ✅ Embedded custom metadata
- ✅ Saved it to file
- ✅ Loaded it back
- ✅ Extracted and displayed metadata

**Full metadata control in ComfyUI!** 🚀

---

## Next: Try The Complete Guide

For detailed explanations, see:
`WORKFLOW_GUIDE_Metadata_Roundtrip.md`

For more workflows, see:
`FFpy_Complete_Workflow_Guide.md`
