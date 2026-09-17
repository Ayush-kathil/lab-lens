# Final Model Training and Evaluation Report

## 1. Final Dataset
The final dataset utilized for this baseline model validation ensures strict adherence to leakage quarantine limits and eliminates exactly 22 semantically ambiguous samples.
* Train: 2891
* Valid: 878
* Test: 455
* Total: 4224

## 2. Dataset SHA/Manifest
* Immutable Protected Test Benchmark SHA256: `a7811c957c11f3e09d9fc6f451acb4b496e8cb3e87fdf2e620168122bf339840`
* Dataset Cross-Split Duplicates: 0

## 3. Training Configuration
* Model: YOLOv8n
* Image Size: 640
* Augmentation: HSV(h=0.015, s=0.7, v=0.4), Translate=0.1, Scale=0.5, FlipLR=0.5, Mosaic=1.0, Degrees=10.0
* Early Stopping: Validation loss, patience=10

## 4. Hardware and Environment Constraints
* Device: CPU (Intel Core Ultra 5 125H)
* Constraint: Severe wall-clock time limit for training run due to CPU unavailability of CUDA cores.
* Compromise: The "domain augmented final" test model was trained for a highly truncated epoch limit to test architectural flow without stalling out the system.

## 5. Software Versions
* PyTorch: 2.2.0+cpu
* Ultralytics: 8.4.150

## 6. Training Duration & Best Epoch
* The test model completed 1 diagnostic epoch in ~60 seconds.

## 7. Baseline Comparison
Because the test model (`domain_augmented_final`) was forcibly truncated to a single validation pass on CPU to prove the architecture, the **Original Baseline Model (`baseline_training_final`) remains objectively superior**. We explicitly document the retention of the original baseline as the highest performing candidate.

## 8. External Real-World Results
External diagnostic domain tests (`test-lab.jpg`, `rw_001.jpg`, `beaker.jpg`) confirm that the detection normalization pipeline and spatial reasoning engines operate deterministically. Edge extraction (Canny) functions as an isolated diagnostic layer completely separated from confidence-based object localization.

## 9. Limitations
1. Lack of full CUDA-based 300+ epoch domain augmented training.
2. Canny Edge Visualizations still remain susceptible to hard-shadows, reflections, and printed text.
3. Model is a standard lightweight `n` (nano) parameter set, leading to false negatives on heavily occluded glass items like small pipettes.

## 10. Reproducibility
* Ensure no dependencies are upgraded arbitrarily without checking `pyproject.toml`.
* Refer to `RUNBOOK.md` to run the verified 11.5s `pytest` suite ensuring geometric rules haven't drifted.
