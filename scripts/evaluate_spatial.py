import argparse
import sys
import yaml
import json
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent / "src"))
from lab_lens.spatial import (
    SetupSpecification, SpatialRule, RuleEngine, BoundingBox, DetectionPosition
)

def load_config(config_path: str) -> tuple:
    with open(config_path, 'r') as f:
        data = yaml.safe_load(f)
        
    regions = {
        name: BoundingBox(r['x1'], r['y1'], r['x2'], r['y2'])
        for name, r in data.get('regions', {}).items()
    }
    
    spec = SetupSpecification(
        setup_name=data['setup_name'],
        required_objects=data.get('required_objects', {}),
        regions=regions
    )
    
    rules = []
    for r in data.get('spatial_rules', []):
        rules.append(SpatialRule(
            rule_type=r['rule_type'],
            subject_class=r['subject_class'],
            target=r['target'],
            threshold=r.get('threshold')
        ))
        
    return spec, rules

def load_detections(json_path: str) -> list:
    with open(json_path, 'r') as f:
        data = json.load(f)
        
    detections = []
    for d in data:
        box = BoundingBox(d['x1'], d['y1'], d['x2'], d['y2'])
        detections.append(DetectionPosition(
            box=box, 
            class_name=d['class_name'], 
            confidence=d.get('confidence', 1.0)
        ))
    return detections

def main():
    parser = argparse.ArgumentParser(description="Evaluate spatial compliance.")
    parser.add_argument('--config', required=True, help="Path to spatial configuration YAML")
    parser.add_argument('--detections', required=True, help="Path to detections JSON")
    args = parser.parse_args()

    spec, rules = load_config(args.config)
    detections = load_detections(args.detections)
    
    engine = RuleEngine(spec, rules)
    result = engine.evaluate(detections)
    
    print("========================================")
    print("       SPATIAL COMPLIANCE RESULT        ")
    print("========================================")
    print(f"Setup      : {spec.setup_name}")
    print(f"Compliant  : {result.compliant}")
    
    if result.satisfied_rules:
        print("\n--- Satisfied Rules ---")
        for s in result.satisfied_rules:
            print(f"  [+] {s}")
            
    if not result.compliant:
        print("\n--- Violations ---")
        for v in result.violations:
            print(f"  [-] {v.violation_type}: {v.message}")
            
if __name__ == '__main__':
    main()
