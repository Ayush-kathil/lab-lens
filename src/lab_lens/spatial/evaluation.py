import json
from dataclasses import dataclass
from typing import Dict, List, Any
from .core import BoundingBox, DetectionPosition
from .engine import SetupSpecification, SpatialRule, RuleEngine

@dataclass
class EvaluationReport:
    total_samples: int
    exact_matches: int
    incorrect_samples: List[str]
    compliance_accuracy: float

class SpatialEvaluationHarness:
    @staticmethod
    def evaluate_dataset(json_path: str) -> EvaluationReport:
        with open(json_path, 'r') as f:
            data = json.load(f)
            
        incorrect = []
        
        for sample in data:
            # Reconstruct specification
            setup = sample['setup_specification']
            regions = {
                name: BoundingBox(r['x1'], r['y1'], r['x2'], r['y2'])
                for name, r in setup['regions'].items()
            }
            spec = SetupSpecification(
                setup_name=setup['setup_name'],
                required_objects=setup['required_objects'],
                regions=regions
            )
            
            rules = []
            for r in setup['spatial_rules']:
                rules.append(SpatialRule(
                    rule_type=r['rule_type'],
                    subject_class=r['subject_class'],
                    target=r['target'],
                    threshold=r.get('threshold')
                ))
                
            engine = RuleEngine(spec, rules)
            
            # Reconstruct detections
            detections = []
            for obj in sample['objects']:
                box = BoundingBox(obj['box']['x1'], obj['box']['y1'], obj['box']['x2'], obj['box']['y2'])
                detections.append(DetectionPosition(box, obj['class_name'], obj.get('confidence', 1.0)))
                
            # Predict
            result = engine.evaluate(detections)
            
            # Compare with ground truth oracle
            expected = sample['expected_output']
            
            match = True
            if result.compliant != expected['compliant']:
                match = False
            else:
                # Compare violations
                pred_v_types = sorted([v.violation_type.value for v in result.violations])
                exp_v_types = sorted([v['type'] for v in expected['violations']])
                if pred_v_types != exp_v_types:
                    match = False
                    
            if not match:
                incorrect.append(sample['sample_id'])
                
        total = len(data)
        matches = total - len(incorrect)
        
        return EvaluationReport(
            total_samples=total,
            exact_matches=matches,
            incorrect_samples=incorrect,
            compliance_accuracy=matches / total if total > 0 else 0.0
        )
