# Lab Lens Algorithms

## Preprocessing: Image Quality Analysis
**Why it is used:** To ensure that images fed into the pipeline meet minimum criteria for confident detection. Degraded images can lead to false negatives or inaccurate spatial mapping.
**Input:** Raw image array (BGR format).
**Output:** An `ImageQualityResult` object containing metrics and a PASS/WARNING/FAIL status.

**Algorithmic Principle:**
1. **Brightness:** Mean intensity of the grayscale image. A value outside `[40, 220]` triggers a warning.
2. **Contrast:** Standard deviation of the grayscale image. Evaluates dynamic range. Values below `20` indicate low contrast.
3. **Blur:** Variance of the Laplacian of the grayscale image (`cv2.Laplacian`). High variance indicates sharp edges; low variance (< `100`) triggers a `HIGH_BLUR` warning.
4. **Resolution:** Direct width/height bounds check against configuration.

**Limitations:**
These are heuristic engineering thresholds, not learned metrics. They may flag intentionally low-light but viable setups as WARNINGs, and the Laplacian variance depends heavily on image content (a completely empty white lab table might register as blurry due to lack of edges).

## Preprocessing: Enhancement (Optional)
**Why it is used:** To correct degraded images identified by the quality analysis before detection.
**Input:** BGR image array.
**Output:** Enhanced BGR image array.

**Implementation:**
- **Resizing:** `cv2.resize` with aspect ratio preservation (using interpolation `INTER_AREA`).
- **Contrast Enhancement:** Contrast Limited Adaptive Histogram Equalization (CLAHE) applied to the Lightness channel of the LAB color space.
- **Denoising:** OpenCV's Fast Non-Local Means Denoising (`cv2.fastNlMeansDenoisingColored`).
