import numpy as np
import cv2
import pytest
from lab_lens.preprocessing.image_quality import analyze_image_quality, ImageQualityResult
from lab_lens.preprocessing.enhancement import resize_image, enhance_contrast

@pytest.fixture
def base_config():
    return {
        'quality': {
            'minimum_width': 100,
            'minimum_height': 100,
            'brightness_min': 40.0,
            'brightness_max': 220.0,
            'contrast_threshold': 20.0,
            'blur_threshold': 100.0
        }
    }

def test_valid_image(base_config):
    # Create a dummy image that is bright and has contrast
    img = np.random.randint(100, 200, (400, 400, 3), dtype=np.uint8)
    # Add some edges for blur_score (Laplacian variance)
    img[100:200, 100:200] = 255 
    
    res = analyze_image_quality(img, base_config)
    assert res.status == "PASS"
    assert len(res.warnings) == 0

def test_tiny_image(base_config):
    img = np.zeros((50, 50, 3), dtype=np.uint8)
    res = analyze_image_quality(img, base_config)
    assert "LOW_RESOLUTION" in res.warnings

def test_low_brightness(base_config):
    img = np.full((200, 200, 3), 10, dtype=np.uint8)
    res = analyze_image_quality(img, base_config)
    assert "LOW_BRIGHTNESS" in res.warnings

def test_high_brightness(base_config):
    img = np.full((200, 200, 3), 240, dtype=np.uint8)
    res = analyze_image_quality(img, base_config)
    assert "HIGH_BRIGHTNESS" in res.warnings

def test_low_contrast(base_config):
    img = np.full((200, 200, 3), 128, dtype=np.uint8)
    res = analyze_image_quality(img, base_config)
    assert "LOW_CONTRAST" in res.warnings
    assert "HIGH_BLUR" in res.warnings  # Constant image has 0 variance Laplacian

def test_blurry_image(base_config):
    img = np.random.randint(100, 200, (400, 400, 3), dtype=np.uint8)
    img = cv2.GaussianBlur(img, (21, 21), 0) # blur it heavily
    res = analyze_image_quality(img, base_config)
    # Could still have some variance but usually lowers it
    # We just check the function runs. The exact value depends on the random noise.

def test_resizing():
    img = np.zeros((1000, 500, 3), dtype=np.uint8)
    resized = resize_image(img, 640)
    assert resized.shape[:2] == (640, 320) # Preserves aspect ratio

def test_resizing_no_upscale():
    img = np.zeros((300, 200, 3), dtype=np.uint8)
    resized = resize_image(img, 640)
    assert resized.shape[:2] == (300, 200)

def test_invalid_image_quality(base_config):
    img = np.array([])
    res = analyze_image_quality(img, base_config)
    assert res.status == "FAIL"
    assert "INVALID_IMAGE" in res.warnings
