# VITyarthi Report Evidence Mapping

This document maps the official VITyarthi project report requirements to actual, reproducible artifacts and commands within the Lab Lens repository. 

| Report Requirement | Evidence Source | Repository File / Execution Command | Expected Outcome |
|:---|:---|:---|:---|
| **1. Cover Page** | Project Title & Author | `statement.md` & `README.md` | Standard cover info |
| **2. Introduction** | Overview & Scope | `README.md` (Sections 1-3), `statement.md` | Prototype description |
| **3. Problem Statement** | Core Problem | `statement.md` | Laboratory setup verification complexity |
| **4. Functional Requirements** | Implemented Modules | `README.md` (Section 5) | FR-01 through FR-10 |
| **5. Non-functional Reqs** | System Traits | `README.md` (Section 6) | Reliability, Reproducibility, Determinism, Error Handling |
| **6. System Architecture** | Component Graph | `README.md` (Section 8) | Mermaid Architecture Diagram |
| **7. Design Diagrams** | Process/Workflow | `README.md` (Section 7) | Mermaid Workflow Diagram |
| **8. Design Decisions** | Engineering Choices | `docs/REPORT_ENGINEERING_CHALLENGES.md` | Rationale on dataset repair, spatial relations |
| **9. Implementation Details**| Tech Stack & Structure | `README.md` (Sections 9, 14, 19) | Python, YOLO, OpenCV, Spatial geometric logic |
| **10. Screenshots/Results** | Terminal Output | `docs/REPORT_SCREENSHOT_CHECKLIST.md` | Real CLI evidence (Compliant, Non-compliant, Unspecified) |
| **11. Testing Approach** | Pytest Suite | `pytest tests/` | E2E pipeline, unit tests, robustness |
| **12. Challenges Faced** | Implementation Hurdles | `docs/REPORT_ENGINEERING_CHALLENGES.md` | Data leakage, unreadable images, invalid bounds |
| **13. Learnings** | Key Takeaways | `docs/REPORT_LEARNINGS.md` | Dataset forensics, object vs spatial ground truth |
| **14. Future Enhancements** | Limitations/Future | `README.md` (Sections 27, 28) | Real-world benchmark, GPU scaling |
| **15. References** | Citations | `docs/REPORT_REFERENCES.md` | ChemEq25, Ultralytics YOLO |

## Model Selection & Evaluation Methodology
- **Rationale**: Documented in `README.md` (Section 11). YOLOv8n chosen for CPU-friendly prototyping.
- **Detector Metrics**: Extracted from Epoch 3 Validation and Held-out test logs. See `docs/REPORT_RESULTS.md`.
- **Spatial Evaluation**: Evaluated against 21 deterministic synthetic fixtures.
- **Pipeline Integration**: Evaluated end-to-end on 16 AI Silver Label images. No human real-world ground truth is claimed.
