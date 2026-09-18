# ChemEq25 Dataset Forensic Pairing Report

## 1. Archive Inventory
- **Path**: `C:\Users\shiva\Downloads\ChemEq25 (Main paper Scientific Data journal, Titl.zip`
- **Size**: 147 MB
- **Total Entries**: 9,200 files
- **Structure**: Roboflow standard YOLO format (`train/`, `valid/`, `test/` containing `images/` and `labels/`).
- **Metadata Files Found**: `data.yaml`, `Metadata.csv`

## 2. Metadata Findings
- `data.yaml` contains class definitions and a Roboflow export URL (`https://universe.roboflow.com/dip-project-cktfe/chemistry-lab-apparatus-detn/dataset/8`).
- `Metadata.csv` contains a canonical mapping of long filenames to bounding boxes (Columns: `Image, Set, Class_ID, Class_Name, X, Y, Width, Height`).

## 3. Filename Findings
- The original ZIP archive *itself* contains Windows 8.3 short-filenames (e.g., `IM1A7B~1.JPG`, `20B299~1.TXT`). The dataset creator compressed these truncated names directly into the archive.
- The short filenames for an image and its corresponding label **do not match** (e.g., `20B299~1.TXT` has no corresponding `20B299~1.JPG`). This occurs because the Windows NTFS 8.3 collision hash generation algorithm factors in the file extension, resulting in different hex hashes for `.jpg` and `.txt` files with identical long stems.

## 4. ZIP Ordering Findings
- The files within the ZIP are grouped entirely by directory (e.g., all test images, then all test labels).
- They are **not** adjacent (no image is followed immediately by its corresponding label). 
- ZIP ordering provides zero evidence of pairing.

## 5. Annotation / Image Content Correlation
- We can map a truncated label file (e.g., `20B299~1.TXT`) to its original long filename using the unique bounding box coordinates listed in `Metadata.csv`.
- **However**, there is zero data embedded in the truncated `.JPG` files (no EXIF metadata, no embedded strings) to link them back to their long filenames or their bounding boxes.
- Therefore, the bridge between the physical image file and its ground truth is completely severed.

## 6. COCO / YOLO Cross-Validation
- No COCO JSON files or alternate annotation formats exist in the archive. 

## 7. Dataset Source Documentation
- The dataset was generated via Roboflow, which explains the long `_jpg.rf.[hash].jpg` names that ultimately triggered the NTFS path-length/collision truncation on the creator's machine before zipping.

## 8. Status of the 66 Invalid Labels
- The 6 `empty_file` labels represent valid negative samples (background images).
- The 60 `wrong_number_of_fields` labels are genuinely corrupted lines. 
- Due to the pairing impossibility, cleaning these is irrelevant.

## 9. Critical Discovery on Alphabetical Sorting
Even if alphabetical sorting were permitted, it would fail catastrophically. Because the 8.3 short names are generated using a hexadecimal hash of the long name, their alphabetical order is entirely randomized compared to the original chronological/alphabetical order of the long filenames. **Sequential pairing would assign random labels to random images.**

## 10. Final Recommendation
**NOT_SAFE_FOR_RECONSTRUCTION**

**Conclusion:** The dataset archive is mathematically corrupted. The loss of the original filenames in the images, combined with the divergent hashing of the labels, permanently destroys the image-to-label mapping. 
