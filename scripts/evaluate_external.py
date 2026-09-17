import cv2
import hashlib
from ultralytics import YOLO
from lab_lens.pipeline import LabLensPipeline

images = {
    'test-lab.jpg': 'test-lab.jpg',
    'rw_001.jpg': 'Dataset/SpatialComplianceReal/images/rw_001.jpg',
    'beaker.jpg': 'outputs/dataset_audit/montages/Beaker.jpg'
}

model_path = 'runs/detect/outputs/baseline_training_final/weights/best.pt'
yolo = YOLO(model_path)
pipeline = LabLensPipeline(model_path=model_path)

with open(model_path, 'rb') as f:
    model_sha = hashlib.sha256(f.read()).hexdigest()
print(f'MODEL SHA256: {model_sha}\n')

for name, path in images.items():
    print('='*50)
    print(f'IMAGE: {name}')
    print(f'PATH: {path}')
    with open(path, 'rb') as f:
        sha = hashlib.sha256(f.read()).hexdigest()
    img = cv2.imread(path)
    print(f'SHA256: {sha}')
    print(f'DIMENSIONS: {img.shape if img is not None else None}')
    print('='*50)
    
    if img is None:
        continue

    for c in [0.5, 0.25, 0.1, 0.05, 0.01]:
        print(f'\n--- CONFIDENCE {c} ---')
        
        # Direct Ultralytics
        res = yolo(img, conf=c, verbose=False)[0]
        direct_dets = []
        if res.boxes is not None:
            for box in res.boxes:
                conf = float(box.conf[0])
                cls = int(box.cls[0])
                cls_name = yolo.names[cls]
                x1, y1, x2, y2 = box.xyxy[0].tolist()
                direct_dets.append({'class': cls_name, 'conf': conf, 'box': [x1, y1, x2, y2]})
        
        # Pipeline
        pipe_dets = pipeline.detector.predict(img, conf_threshold=c)
        
        print(f'Direct Count   : {len(direct_dets)}')
        print(f'Pipeline Count : {len(pipe_dets)}')
        print(f'Direct Classes : {[d["class"] for d in direct_dets]}')
        print(f'Pipeline Class : {[d.class_name for d in pipe_dets]}')
        print(f'Direct Conf    : {[round(d["conf"], 4) for d in direct_dets]}')
        print(f'Pipeline Conf  : {[round(d.confidence, 4) for d in pipe_dets]}')
