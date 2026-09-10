import cv2
from pathlib import Path

class ValidationError(Exception):
    pass

def validate_image_path(path: str) -> Path:
    img_path = Path(path)
    if not img_path.exists():
        raise ValidationError(f"Image not found at path: {path}")
    
    if not img_path.is_file():
        raise ValidationError(f"Path is not a file: {path}")
        
    ext = img_path.suffix.lower()
    if ext not in ['.jpg', '.jpeg', '.png']:
        raise ValidationError(f"Unsupported image extension '{ext}'. Must be .jpg, .jpeg, or .png")
        
    return img_path

def validate_image_decodable(path: str) -> None:
    # Use OpenCV to verify it can be decoded
    # We use imread directly. In production, this can be slow, but it guarantees validity.
    img = cv2.imread(path)
    if img is None:
        raise ValidationError(f"OpenCV could not decode image at path: {path}")
    if img.shape[0] == 0 or img.shape[1] == 0:
        raise ValidationError(f"Image has invalid dimensions: {img.shape}")
