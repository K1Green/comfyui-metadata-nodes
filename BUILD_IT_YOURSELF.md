# Build the Metadata Workflow Yourself

## Manual Node-by-Node Guide

If you prefer to build the workflow from scratch instead of importing the JSON, follow these steps:

---

## Part 1: Generate & Save (5 nodes)

### 1. Add Firefly Text to Image

**Right-click → Add Node → api node/firefly → Firefly Text to Image**

Settings:
```
prompt: majestic photorealistic snow leopard high on a mountain at sunset with valley below
size: 1024x1024 (1:1)
model_version: image4_standard
num_variations: 1
```

---

### 2. Add Preview Image

**Right-click → Add Node → image → Preview Image**

Connect:
- Firefly `image` → Preview Image `images`

---

### 3. Add FFpy Save with Metadata ⭐

**Right-click → Add Node → api node/photoshop → FFpy Save with Metadata**

Settings:
```
filename_prefix: AI_Snow_Leopard
title: AI Snow Leopard
description: majestic photorealistic snow leopard high on a mountain at sunset with valley below
keywords: AI, Firefly, Wildlife
creator: Kevin Green
copyright: 2025
rating: 5
label: Blue
output_path: (leave empty for default)
```

Connect:
- Firefly `image` → Save with Metadata `image`

---

### 4. Add Show Text (Save Debug Log)

**Right-click → Add Node → utils → Show Text** (pysssss)

Connect:
- Save with Metadata `debug_log` → Show Text `text`

Rename node: "Show Save Debug Log"

---

## Part 2: Load from Folder (4 nodes)

### 5. Add FFpy Load Image from Folder ⭐

**Right-click → Add Node → api node/photoshop → FFpy Load Image from Folder**

Settings:
```
folder_path: /Users/kevin/Applications/Development/ComfyUI/output
file_pattern: AI_Snow_Leopard*.png
sort_by: date_modified
sort_order: descending
image_index: 0
recursive: false
```

**NO connections needed** - This node finds files automatically!

---

### 6. Add Preview Image (Loaded)

**Right-click → Add Node → image → Preview Image**

Connect:
- Load Image from Folder `image` → Preview Image `images`

Rename node: "Preview Loaded Image"

---

### 7. Add Show Text (Load Debug Log)

**Right-click → Add Node → utils → Show Text** (pysssss)

Connect:
- Load Image from Folder `debug_log` → Show Text `text`

Rename node: "Show Load Debug Log"

---

### 8. Add Show Text (Filename)

**Right-click → Add Node → utils → Show Text** (pysssss)

Connect:
- Load Image from Folder `filename` → Show Text `text`

Rename node: "Show Filename"

---

## Part 3: Read Metadata (5 nodes)

### 9. Add FFpy ExifTool (Read All) ⭐

**Right-click → Add Node → api node/photoshop → FFpy ExifTool (Advanced Metadata)**

Settings:
```
operation: Read All Metadata
output_format: Pretty JSON
group_filter: (leave empty)
include_binary: false
extract_embedded: false
```

Connect:
- Load Image from Folder `image` → ExifTool `image`
- Load Image from Folder `file_path` → ExifTool `file_path` ⭐ (CRITICAL: reads metadata from actual file!)

Rename node: "ExifTool - Read All Metadata"

---

### 10. Add Show Text (All Metadata JSON)

**Right-click → Add Node → utils → Show Text** (pysssss)

Connect:
- ExifTool (Read All) `metadata_json` → Show Text `text`

Rename node: "Show All Metadata (JSON)"

---

### 11. Add Show Text (ExifTool Debug Log)

**Right-click → Add Node → utils → Show Text** (pysssss)

Connect:
- ExifTool (Read All) `debug_log` → Show Text `text`

Rename node: "Show ExifTool Debug Log"

---

### 12. Add FFpy ExifTool (Read Specific) ⭐

**Right-click → Add Node → api node/photoshop → FFpy ExifTool (Advanced Metadata)**

Settings:
```
operation: Read Specific Tags
output_format: Human Readable
tag_names:
  Title
  Description
  Author
  Copyright
  Subject
```

**IMPORTANT:** For `tag_names`, press Enter after each tag name to put them on separate lines!

Connect:
- Load Image from Folder `image` → ExifTool `image`
- Load Image from Folder `file_path` → ExifTool `file_path` ⭐ (CRITICAL: reads metadata from actual file!)

Rename node: "ExifTool - Read Specific Metadata"

---

### 13. Add Show Text (Your Metadata) ⭐

**Right-click → Add Node → utils → Show Text** (pysssss)

Connect:
- ExifTool (Read Specific) `metadata_json` → Show Text `text`

Rename node: "Show Specific Metadata (Readable)"

**THIS IS YOUR FINAL OUTPUT** - Shows your metadata!

---

## Final Connection Diagram

```
Firefly (1)
  ├─→ Preview (2)
  └─→ Save with Metadata (3)
       ├─→ Show Save Log (4)

Load from Folder (5)
  ├─→ Preview Loaded (6)
  ├─→ Show Load Log (7)
  ├─→ Show Filename (8)
  ├─→ ExifTool All (9)
  │    ├─→ Show All JSON (10)
  │    └─→ Show ExifTool Log (11)
  └─→ ExifTool Specific (12)
       └─→ Show Your Metadata (13) ⭐
```

---

## Key Settings Reference

### Node 3: Save with Metadata
```yaml
filename_prefix: AI_Snow_Leopard
title: AI Snow Leopard
keywords: AI, Firefly, Wildlife
creator: Kevin Green
copyright: 2025
rating: 5
label: Blue
```

### Node 5: Load from Folder
```yaml
folder_path: /Users/kevin/Applications/Development/ComfyUI/output
file_pattern: AI_Snow_Leopard*.png
sort_by: date_modified
sort_order: descending
image_index: 0
```

### Node 12: ExifTool Specific
```yaml
operation: Read Specific Tags
output_format: Human Readable
tag_names: (one per line)
  Title
  Description
  Author
  Copyright
  Subject
```

---

## Testing Your Build

### Run Order (Automatic)

1. Queue Prompt
2. Firefly generates → Save → Load → ExifTool → Display
3. All happens automatically!

### What to Check

| Node | Check This |
|------|-----------|
| **2** | See generated image |
| **4** | See "7 metadata fields" |
| **6** | See same image |
| **8** | See filename |
| **13** | **See YOUR metadata!** |

---

## Troubleshooting Build

### Connection Not Working?

- Check output type matches input type
- IMAGE → IMAGE
- STRING → STRING (text)

### Node Missing?

**Restart ComfyUI** and check:
- `api node/photoshop` category
- Look for "FFpy" nodes

### Show Text Not Available?

Install ComfyUI-Custom-Scripts:
```bash
cd custom_nodes
git clone https://github.com/pythongosssss/ComfyUI-Custom-Scripts
```

Or use built-in "SaveText" node instead

---

## Layout Tips

### Organize Left to Right

```
[Left]          [Middle]         [Right]
Generate  →  Save & Load  →  Read & Display
(Nodes 1-2)   (Nodes 3-8)    (Nodes 9-13)
```

### Group by Function

1. **Generation** (top)
2. **Storage** (middle)
3. **Retrieval** (bottom)

### Color Code

- 🔴 Firefly node = Red
- 🟢 FFpy nodes = Green
- 🔵 Display nodes = Blue

---

## Common Mistakes

### ❌ Wrong: Only connecting image without file_path

ExifTool has THREE inputs:
- `image` - Optional, for pass-through visualization
- `file_path` - **CRITICAL!** Path to actual file with metadata
- `operation` - What to do (Read All, Read Specific, Write)

**You MUST connect BOTH:**
1. `image` for visualization
2. `file_path` for reading metadata from the actual saved file

**Why?** The image tensor doesn't contain metadata - only the saved PNG file has it!

### ❌ Wrong: Not setting tag_names properly

Must be **one per line**:
```
Title
Description
Author
```

NOT:
```
Title, Description, Author
```

### ❌ Wrong: Different folder paths

Node 3 `output_path` must match Node 5 `folder_path`

---

## Success Checklist

Built correctly when:

- ✅ 13 nodes total
- ✅ 7 Show Text nodes (4, 7, 8, 10, 11, 13)
- ✅ 2 Preview Image nodes (2, 6)
- ✅ 2 ExifTool nodes (9, 12)
- ✅ 1 Firefly node (1)
- ✅ 1 Save node (3)
- ✅ 1 Load node (5)

---

## Final Test

After building, run and check:

1. ✅ Node 2 shows snow leopard
2. ✅ Node 4 shows "saved successfully"
3. ✅ Node 6 shows same image
4. ✅ Node 8 shows "AI_Snow_Leopard_*.png"
5. ✅ **Node 13 shows:**
   ```
   Title: AI Snow Leopard
   Author: Kevin Green
   Copyright: 2025
   Subject: AI, Firefly, Wildlife
   ```

**If all ✅, you built it correctly!** 🎉

---

## Alternative: Import Instead

Don't want to build manually? Just import:

**Drag this file into ComfyUI:**
`workflow_metadata_roundtrip.json`

Instant workflow! 🚀

---

## Next Steps

Once working:

1. **Customize** - Change prompt, metadata
2. **Experiment** - Try different settings
3. **Expand** - Add more processing nodes
4. **Share** - Save your version

**You now have complete metadata control!** ✨
