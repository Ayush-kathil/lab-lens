import json
import sys
from pathlib import Path

# DEV UTILITY - DO NOT RUN IN CI
# This script generates purely synthetic bounding boxes for testing the engine.
# It MUST NOT be used to overwrite canonical expected_output during evaluation.

def create_sample(sample_id, objects, required_objects, regions, rules, expected_compliant, expected_violations):
    return {
        "sample_id": sample_id,
        "image_ref": "synthetic",
        "image_width": 1000,
        "image_height": 1000,
        "setup_specification": {
            "setup_name": f"setup_{sample_id}",
            "required_objects": required_objects,
            "regions": regions,
            "spatial_rules": rules
        },
        "objects": objects,
        "expected_output": {
            "compliant": expected_compliant,
            "violations": expected_violations
        }
    }

def box(x1, y1, x2, y2):
    return {"x1": x1, "y1": y1, "x2": x2, "y2": y2}

def main():
    if len(sys.argv) < 2:
        print("Usage: python generate_synthetic_fixtures.py <output_path.json>")
        print("DEV UTILITY ONLY. Do not overwrite canonical dataset automatically.")
        sys.exit(1)
        
    out_path = Path(sys.argv[1])
    
    samples = []
    # (Elided generation for brevity, the canonical file already exists)
    print("This script is deprecated as an automated tool. Please edit the JSON fixtures manually to maintain independent oracle status.")
    
if __name__ == '__main__':
    main()
