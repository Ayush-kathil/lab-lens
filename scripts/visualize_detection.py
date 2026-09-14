import argparse
import cv2
import os
import sys
from lab_lens.detection.inference import YOLODetector

def main():
    parser = argparse.ArgumentParser(description="Generate Visual Evidence from YOLOv8 inference")
    parser.add_argument("--image", required=True, help="Path to input image")
    parser.add_argument("--model", required=True, help="Path to best.pt")
    parser.add_argument("--outdir", default="outputs/visualizations", help="Output directory")
    args = parser.parse_args()

    if not os.path.exists(args.image):
        print(f"Error: Image {args.image} not found.")
        sys.exit(1)
    if not os.path.exists(args.model):
        print(f"Error: Model {args.model} not found.")
        sys.exit(1)

    os.makedirs(args.outdir, exist_ok=True)

    print(f"Loading image: {args.image}")
    img = cv2.imread(args.image)
    if img is None:
        print("Error: Could not read image.")
        sys.exit(1)
        
    print(f"Loading model: {args.model}")
    try:
        detector = YOLODetector()
        detector.load_model(args.model)
    except Exception as e:
        print(f"Failed to load model: {e}")
        sys.exit(1)

    print("Running inference...")
    detections = detector.predict(img)

    print(f"Detected {len(detections)} objects:")
    
    # 1. YOLO Detection Visualization
    img_yolo = img.copy()
    for d in detections:
        print(f" - {d.class_name} ({d.confidence:.2f}) at [{d.x1:.1f}, {d.y1:.1f}, {d.x2:.1f}, {d.y2:.1f}]")
        x1, y1, x2, y2 = int(d.x1), int(d.y1), int(d.x2), int(d.y2)
        cv2.rectangle(img_yolo, (x1, y1), (x2, y2), (0, 255, 0), 2)
        label = f"{d.class_name} {d.confidence:.2f}"
        (w, h), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
        cv2.rectangle(img_yolo, (x1, y1 - h - 5), (x1 + w, y1), (0, 255, 0), -1)
        cv2.putText(img_yolo, label, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)

    yolo_path = os.path.join(args.outdir, "test_lab_yolo_detection.jpg")
    cv2.imwrite(yolo_path, img_yolo)
    print(f"Saved YOLO visualization to: {yolo_path}")

    # 2. Edge / Contour Visualization
    print("Running edge detection (Canny)...")
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_blur = cv2.GaussianBlur(img_gray, (5, 5), 0)
    edges = cv2.Canny(img_blur, 50, 150)
    
    edge_path = os.path.join(args.outdir, "test_lab_edges.jpg")
    cv2.imwrite(edge_path, edges)
    print(f"Saved Edge visualization to: {edge_path}")
    
    # 3. Combined Visualization
    print("Running combined visualization...")
    # Convert edges back to BGR so we can overlay green boxes
    img_combined = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
    for d in detections:
        x1, y1, x2, y2 = int(d.x1), int(d.y1), int(d.x2), int(d.y2)
        cv2.rectangle(img_combined, (x1, y1), (x2, y2), (0, 255, 0), 2)
        label = f"{d.class_name} {d.confidence:.2f}"
        (w, h), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
        cv2.rectangle(img_combined, (x1, y1 - h - 5), (x1 + w, y1), (0, 255, 0), -1)
        cv2.putText(img_combined, label, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
        
    combined_path = os.path.join(args.outdir, "test_lab_combined.jpg")
    cv2.imwrite(combined_path, img_combined)
    print(f"Saved Combined visualization to: {combined_path}")

    print("Visualization generation complete.")

if __name__ == "__main__":
    main()
