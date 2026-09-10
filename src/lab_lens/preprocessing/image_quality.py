from dataclasses import dataclass
from typing import List
import cv2
import numpy as np

@dataclass
class ImageQualityResult:
    width: int
    height: int
    brightness: float
    contrast: float
    blur_score: float
    status: str
    warnings: List[str]

def analyze_image_quality(img: np.ndarray, config: dict) -> ImageQualityResult:
    """
    Analyzes an image and returns an ImageQualityResult containing metrics and warnings.
    """
    warnings = []
    status = "PASS"
    
    if img is None or img.size == 0:
        return ImageQualityResult(0, 0, 0.0, 0.0, 0.0, "FAIL", ["INVALID_IMAGE"])

    h, w = img.shape[:2]
    
    # Mathematical rationale:
    # Brightness = mean of the grayscale image. Ranges 0 (black) to 255 (white).
    # Contrast = standard deviation of the grayscale image. Low std means narrow intensity range (low contrast).
    # Blur = variance of the Laplacian. Edges have high Laplacian response. A blurry image lacks edges.
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) if len(img.shape) == 3 else img
    
    brightness = float(np.mean(gray))
    contrast = float(np.std(gray))
    blur_score = float(np.var(cv2.Laplacian(gray, cv2.CV_64F)))
    
    q_config = config.get('quality', {})
    min_w = q_config.get('minimum_width', 100)
    min_h = q_config.get('minimum_height', 100)
    bright_min = q_config.get('brightness_min', 40.0)
    bright_max = q_config.get('brightness_max', 220.0)
    contrast_thresh = q_config.get('contrast_threshold', 20.0)
    blur_thresh = q_config.get('blur_threshold', 100.0)
    
    if w < min_w or h < min_h:
        warnings.append("LOW_RESOLUTION")
        status = "WARNING"
        
    if brightness < bright_min:
        warnings.append("LOW_BRIGHTNESS")
        status = "WARNING"
    elif brightness > bright_max:
        warnings.append("HIGH_BRIGHTNESS")
        status = "WARNING"
        
    if contrast < contrast_thresh:
        warnings.append("LOW_CONTRAST")
        status = "WARNING"
        
    if blur_score < blur_thresh:
        warnings.append("HIGH_BLUR")
        status = "WARNING"
        
    if "LOW_RESOLUTION" in warnings and "HIGH_BLUR" in warnings:
        # Too degraded to process reliably
        status = "FAIL"
        
    return ImageQualityResult(
        width=w,
        height=h,
        brightness=brightness,
        contrast=contrast,
        blur_score=blur_score,
        status=status,
        warnings=warnings
    )
