import sys
import os

try:
    from ultralytics import YOLO
except ImportError:
    print("Ultralytics not installed.")
    sys.exit(1)

model = YOLO('yolov8n.pt')

results = model.train(
    data=os.path.abspath('Dataset/ChemEq25_training/data.yaml'),
    epochs=1,
    patience=1,
    batch=32,
    imgsz=160,
    device='cpu',
    workers=0,
    project='runs/detect/outputs',
    name='retrained_model_v1',
    seed=42,
    deterministic=True,
    hsv_h=0.015,
    hsv_s=0.7,
    hsv_v=0.4,
    degrees=10.0,
    translate=0.1,
    scale=0.5,
    shear=0.0,
    perspective=0.0,
    flipud=0.0,
    fliplr=0.5,
    mosaic=1.0,
    mixup=0.0
)

# Eval on test set
metrics = model.val(data=os.path.abspath('Dataset/ChemEq25_training/data.yaml'), split='test')
print("Test metrics:", metrics.box.map50)
