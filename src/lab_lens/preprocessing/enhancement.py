import cv2
import numpy as np

def resize_image(img: np.ndarray, target_size: int) -> np.ndarray:
    """
    Resizes an image such that its longest side matches target_size, 
    preserving aspect ratio.
    """
    if img is None or img.size == 0:
        return img
        
    h, w = img.shape[:2]
    scale = target_size / max(h, w)
    
    if scale >= 1.0:
        return img  # Don't upscale unnecessarily
        
    new_w = int(w * scale)
    new_h = int(h * scale)
    return cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_AREA)

def enhance_contrast(img: np.ndarray) -> np.ndarray:
    """
    Enhances contrast using CLAHE (Contrast Limited Adaptive Histogram Equalization)
    on the L-channel of the LAB color space.
    """
    if len(img.shape) != 3:
        return img
        
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    cl = clahe.apply(l)
    
    merged = cv2.merge((cl, a, b))
    return cv2.cvtColor(merged, cv2.COLOR_LAB2BGR)

def denoise_image(img: np.ndarray) -> np.ndarray:
    """
    Applies a fast Non-Local Means Denoising.
    """
    if len(img.shape) == 3:
        return cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 21)
    else:
        return cv2.fastNlMeansDenoising(img, None, 10, 7, 21)
