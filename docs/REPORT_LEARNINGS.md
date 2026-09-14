# Learnings & Key Takeaways

The development of Lab Lens provided substantial technical and architectural learnings across computer vision, dataset engineering, and software design.

### 1. Importance of Dataset Forensics
Before this project, the assumption was that published datasets (like ChemEq25) were pre-cleaned and benchmark-ready. Discovering exact duplicate images leaking across the train and test splits demonstrated that blind trust in raw datasets leads to flawed, overly optimistic evaluation metrics. Developing the hashing and repair pipeline emphasized that rigorous data forensics is just as critical as model architecture.

### 2. Geometric Reasoning vs. Model Inference
While deep learning handles object detection excellently, verifying spatial compliance (e.g., "is the beaker left of the flask?") is better served by deterministic, transparent geometric reasoning. Abstracting YOLO detections into a normalized Cartesian plane allowed us to write hard, explainable mathematical rules rather than attempting to train a "black box" model to guess compliance.

### 3. Rule-Based Explainability
In safety-adjacent environments, providing a single probability score is insufficient. A major takeaway was the necessity of rule-based explainability. By forcing the spatial engine to explicitly list violations (e.g., "Missing Stand", "Beaker fails left_of relation"), the system became significantly easier to debug and substantially more useful as a feedback mechanism for the end user.

### 4. CPU Resource Management & E2E Profiling
Integrating a full pipeline—from image file decoding to blur analysis, deep learning inference, spatial mathematics, and JSON serialization—highlighted execution bottlenecks. Profiling the pipeline revealed that spatial logic executed in fractions of a millisecond (~0.0001s), while the object detector dominated the runtime (~1.27s). This learning drove the architectural decision to use YOLOv8n (nano) rather than larger, slower models, prioritizing end-to-end responsiveness for the prototype.

### 5. AI Silver Labels vs. Human Ground Truth
The project required evaluating the integrated pipeline on real-world laboratory photographs, but no human-verified spatial ground truth existed for them. Using the detector itself to generate `SILVER_LABEL` annotations to test the pipeline flow was a practical breakthrough. However, strictly separating this AI-generated proxy data from true benchmark accuracy claims reinforced critical scientific integrity and ethical ML reporting standards.
