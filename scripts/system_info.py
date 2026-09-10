import platform
import sys
import psutil
import subprocess

def get_sys_info():
    info = {
        "OS": f"{platform.system()} {platform.release()} ({platform.version()})",
        "Python": sys.version.replace('\n', ''),
        "Executable": sys.executable,
        "CPU": platform.processor() or "Unknown",
        "RAM": f"{psutil.virtual_memory().total / (1024**3):.2f} GB",
        "GPU": "NOT AVAILABLE",
        "GPU_Memory": "NOT AVAILABLE",
        "CUDA": "NOT AVAILABLE",
        "CUDA_Version": "NOT AVAILABLE",
        "PyTorch": "NOT AVAILABLE",
        "OpenCV": "NOT AVAILABLE",
        "NumPy": "NOT AVAILABLE",
        "Ultralytics": "NOT AVAILABLE"
    }

    try:
        import torch
        info["PyTorch"] = torch.__version__
        if torch.cuda.is_available():
            info["CUDA"] = "AVAILABLE"
            info["CUDA_Version"] = torch.version.cuda
            info["GPU"] = torch.cuda.get_device_name(0)
            info["GPU_Memory"] = f"{torch.cuda.get_device_properties(0).total_memory / (1024**3):.2f} GB"
    except ImportError:
        pass

    try:
        import cv2
        info["OpenCV"] = cv2.__version__
    except ImportError:
        pass

    try:
        import numpy as np
        info["NumPy"] = np.__version__
    except ImportError:
        pass

    try:
        import ultralytics
        info["Ultralytics"] = ultralytics.__version__
    except ImportError:
        pass

    return info

def print_sys_info():
    info = get_sys_info()
    print("========================================")
    print("      LAB LENS HARDWARE & ENVIRONMENT   ")
    print("========================================")
    for k, v in info.items():
        print(f"{k.ljust(15)}: {v}")

if __name__ == '__main__':
    print_sys_info()
