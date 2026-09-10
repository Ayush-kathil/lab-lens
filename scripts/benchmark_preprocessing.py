import time
import argparse
import cv2
import numpy as np
from pathlib import Path

from lab_lens.preprocessing.image_quality import analyze_image_quality
from lab_lens.preprocessing.enhancement import resize_image, enhance_contrast, denoise_image
from lab_lens.config.loader import load_config

def benchmark_preprocessing(dataset_dir: str, config_path: str, samples: int = 10):
    dataset_path = Path(dataset_dir)
    images_dir = dataset_path / "test" / "images"
    
    if not images_dir.exists():
        print(f"Directory not found: {images_dir}")
        return
        
    config = load_config(config_path)
    image_files = list(images_dir.glob("*.JPG")) + list(images_dir.glob("*.jpg"))
    if not image_files:
        print("No images found for benchmarking.")
        return
        
    sample_files = image_files[:samples]
    
    times = {
        'load': [],
        'quality': [],
        'resize': [],
        'contrast': [],
        'denoise': []
    }
    
    print(f"Benchmarking {len(sample_files)} images...")
    
    for f in sample_files:
        # Load
        t0 = time.time()
        img = cv2.imread(str(f))
        times['load'].append(time.time() - t0)
        
        if img is None:
            continue
            
        # Quality
        t0 = time.time()
        analyze_image_quality(img, config)
        times['quality'].append(time.time() - t0)
        
        # Resize
        t0 = time.time()
        img_resized = resize_image(img, 640)
        times['resize'].append(time.time() - t0)
        
        # Contrast
        t0 = time.time()
        enhance_contrast(img_resized)
        times['contrast'].append(time.time() - t0)
        
        # Denoise (heavy)
        t0 = time.time()
        denoise_image(img_resized)
        times['denoise'].append(time.time() - t0)
        
    print("\nBENCHMARK RESULTS (Average Time per Image):")
    print(f"  Load Image     : {np.mean(times['load'])*1000:.2f} ms")
    print(f"  Quality Check  : {np.mean(times['quality'])*1000:.2f} ms")
    print(f"  Resize         : {np.mean(times['resize'])*1000:.2f} ms")
    print(f"  Contrast CLAHE : {np.mean(times['contrast'])*1000:.2f} ms")
    print(f"  Denoise (NLM)  : {np.mean(times['denoise'])*1000:.2f} ms")
    print("\nTotal Base Preprocessing (Load+Quality+Resize):")
    base_time = np.mean(times['load']) + np.mean(times['quality']) + np.mean(times['resize'])
    print(f"  {base_time*1000:.2f} ms / image")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset', required=True)
    parser.add_argument('--config', default='configs/default.yaml')
    parser.add_argument('--samples', type=int, default=10)
    args = parser.parse_args()
    benchmark_preprocessing(args.dataset, args.config, args.samples)
