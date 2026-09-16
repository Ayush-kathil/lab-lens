import sys
import json
import os
import cv2
from ultralytics import YOLO

sys.path.insert(0, os.path.abspath('src'))
from lab_lens.pipeline import LabLensPipeline

images = {
    "test_lab": "test-lab.jpg",
    "beaker_photo": r"C:\Users\shiva\.gemini\antigravity\brain\1553869e-6886-42d4-89fe-134be4302ce1\.user_uploaded\media_1789398296486.png"
}

model_path = "runs/detect/outputs/baseline_training_final/weights/best.pt"
if not os.path.exists(model_path):
    print(f"Model not found: {model_path}")
    sys.exit(1)
model = YOLO(model_path)
print(f"Model classes: {model.names}")
print(f"Model task: {model.task}")

results_dict = {}

for name, img_path in images.items():
    if not os.path.exists(img_path):
        print(f"File not found: {img_path}")
        continue
    
    print(f"\n--- {name} ---")
    img = cv2.imread(img_path)
    h, w = img.shape[:2]
    print(f"Original image size: {w}x{h}")
    
    # 1. Raw YOLO
    raw_res = model(img_path, conf=0.01) # get everything
    raw_boxes = raw_res[0].boxes
    raw_detections = []
    if raw_boxes is not None:
        for i in range(len(raw_boxes)):
            cls_idx = int(raw_boxes.cls[i].item())
            conf = float(raw_boxes.conf[i].item())
            x1, y1, x2, y2 = raw_boxes.xyxy[i].tolist()
            raw_detections.append({
                "class_index": cls_idx,
                "class_name": model.names[cls_idx],
                "confidence": conf,
                "x1": x1, "y1": y1, "x2": x2, "y2": y2
            })
    print(f"Raw detections (conf=0.01): {len(raw_detections)}")

    # 1.5 Diagnostic confidence sweep for test-lab.jpg
    if name == "test_lab":
        print(f"Diagnostic sweep for test_lab:")
        for sweep_conf in [0.50, 0.25, 0.10, 0.05, 0.01]:
            sweep_res = model(img_path, conf=sweep_conf, verbose=False)
            sweep_boxes = sweep_res[0].boxes
            sweep_classes = [model.names[int(c)] for c in sweep_boxes.cls.tolist()] if sweep_boxes else []
            print(f"  thresh {sweep_conf}: {len(sweep_classes)} detections: {sweep_classes}")

    # 2. Lab Lens Pipeline
    pipeline = LabLensPipeline(model_path=model_path, conf_threshold=0.25)
    pl_res = pipeline.run(img_path)
    pl_detections = []
    for d in pl_res.detections:
        pl_detections.append({
            "class_name": d.class_name,
            "confidence": d.confidence,
            "box": d.box.__dict__
        })
    print(f"Pipeline detections (conf=0.25): {len(pl_detections)}")
    
    results_dict[name] = {
        "raw_0_01": raw_detections,
        "pipeline": pl_detections
    }

os.makedirs("outputs/forensics", exist_ok=True)
with open("outputs/forensics/inference.json", "w") as f:
    json.dump(results_dict, f, indent=2)
