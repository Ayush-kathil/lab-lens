import argparse
import sys
import subprocess
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(prog="lab_lens", description="Lab Lens CLI")
    subparsers = parser.add_subparsers(dest="command")

    # validate-dataset
    val_parser = subparsers.add_parser("validate-dataset", help="Validate a dataset structure and annotations")
    val_parser.add_argument("--dataset", required=True, help="Path to dataset")

    # inspect-dataset
    ins_parser = subparsers.add_parser("inspect-dataset", help="Inspect dataset class distribution")
    ins_parser.add_argument("--dataset", required=True, help="Path to dataset")

    # audit-dataset-pairs
    adt_parser = subparsers.add_parser("audit-dataset-pairs", help="Audit dataset pairing 8.3 filenames")
    adt_parser.add_argument("--dataset", required=True, help="Path to dataset")

    # quality
    q_parser = subparsers.add_parser("quality", help="Run image quality analysis")
    q_parser.add_argument("--input", required=True, help="Path to input image")
    q_parser.add_argument("--config", default="configs/default.yaml", help="Path to config file")

    # system-info
    sys_parser = subparsers.add_parser("system-info", help="Print system and hardware information")

    # prepare-dataset
    prep_parser = subparsers.add_parser("prepare-dataset", help="Deterministically repair and prepare dataset")
    prep_parser.add_argument("--source", required=True, help="Path to source dataset")
    prep_parser.add_argument("--output", required=True, help="Path to output derived dataset")

    # verify-dataset
    vf_parser = subparsers.add_parser("verify-dataset", help="Verify the prepared dataset")
    vf_parser.add_argument("--dataset", required=True, help="Path to derived dataset")

    # train
    tr_parser = subparsers.add_parser("train", help="Train the detector")
    tr_parser.add_argument("--dataset", required=True, help="Path to dataset")
    tr_parser.add_argument("--config", required=True, help="Path to training config")
    tr_parser.add_argument("--dry-run", action="store_true", help="Print config without training")
    tr_parser.add_argument("--smoke-test", action="store_true", help="Run a 1-epoch tiny training run")

    # evaluate
    ev_parser = subparsers.add_parser("evaluate", help="Evaluate the detector")
    ev_parser.add_argument("--model", required=True, help="Path to model weights")
    ev_parser.add_argument("--dataset", required=True, help="Path to evaluation dataset")

    # predict
    pr_parser = subparsers.add_parser("predict", help="Run detector prediction")
    pr_parser.add_argument("--model", required=True, help="Path to model weights")
    pr_parser.add_argument("--input", required=True, help="Path to input image")

    # infer
    inf_parser = subparsers.add_parser("infer", help="Run end-to-end Lab Lens pipeline")
    inf_parser.add_argument("--image", required=True, help="Path to input image")
    inf_parser.add_argument("--model", help="Path to YOLO model weights (optional for smoke tests)")
    inf_parser.add_argument("--setup", help="Path to spatial setup config (YAML) (optional)")
    inf_parser.add_argument("--json", action="store_true", help="Output machine-readable JSON")

    args = parser.parse_args()

    def run_script(script_name, *args_list):
        script_path = Path(__file__).parent.parent.parent / "scripts" / script_name
        result = subprocess.run([sys.executable, str(script_path), *args_list])
        if result.returncode != 0:
            sys.exit(result.returncode)

    if args.command == "validate-dataset":
        run_script("validate_dataset.py", "--dataset", args.dataset)
    elif args.command == "inspect-dataset":
        run_script("inspect_dataset.py", "--dataset", args.dataset)
    elif args.command == "audit-dataset-pairs":
        run_script("audit_dataset_pairs.py", "--dataset", args.dataset)
    elif args.command == "system-info":
        run_script("system_info.py")
    elif args.command == "prepare-dataset":
        run_script("prepare_training_dataset.py", "--source", args.source, "--output", args.output)
    elif args.command == "verify-dataset":
        run_script("verify_training_dataset.py", "--dataset", args.dataset)
    elif args.command == "train":
        cmd = ["--dataset", args.dataset, "--config", args.config]
        if args.dry_run: cmd.append("--dry-run")
        if args.smoke_test: cmd.append("--smoke-test")
        run_script("train_detector.py", *cmd)
    elif args.command == "evaluate":
        run_script("evaluate_detector.py", "--model", args.model, "--dataset", args.dataset)
    elif args.command == "predict":
        # inline predict scaffold
        import cv2
        from lab_lens.detection.inference import YOLODetector
        try:
            detector = YOLODetector()
            detector.load_model(args.model)
            img = cv2.imread(args.input)
            if img is None:
                print(f"Error: Could not load image {args.input}")
                sys.exit(1)
            detections = detector.predict(img)
            print("Detected equipment:")
            for d in detections:
                print(f"{d.class_name.ljust(20)} {d.confidence:.2f} ({d.x1:.1f}, {d.y1:.1f}, {d.x2:.1f}, {d.y2:.1f})")
        except Exception as e:
            print(f"Error during prediction: {e}")
            sys.exit(1)
    elif args.command == "infer":
        import json
        from lab_lens.pipeline import LabLensPipeline
        from lab_lens.spatial.engine import SetupSpecification, SpatialRule
        from lab_lens.spatial.core import BoundingBox
        setup_spec = None
        spatial_rules = []
        if args.setup:
            try:
                import json
                with open(args.setup, "r", encoding="utf-8") as f:
                    config = json.load(f)

                regions = {}
                for k, v in config.get("regions", {}).items():
                    regions[k] = BoundingBox(v["x1"], v["y1"], v["x2"], v["y2"])

                setup_spec = SetupSpecification(
                    setup_name=config.get("setup_name", "custom_setup"),
                    required_objects=config.get("required_objects", {}),
                    regions=regions
                )

                for r in config.get("spatial_rules", []):
                    spatial_rules.append(SpatialRule(
                        rule_type=r["rule_type"],
                        subject_class=r["subject_class"],
                        target=r["target"],
                        threshold=r.get("threshold")
                    ))
            except ImportError:
                print("Error: PyYAML not installed.", file=sys.stderr)
                sys.exit(1)
            except Exception as e:
                try:
                    # Fallback to PyYAML if available and it's a YAML file
                    import yaml
                    with open(args.setup, "r", encoding="utf-8") as f:
                        config = yaml.safe_load(f)

                    regions = {}
                    for k, v in config.get("regions", {}).items():
                        regions[k] = BoundingBox(v["x1"], v["y1"], v["x2"], v["y2"])

                    setup_spec = SetupSpecification(
                        setup_name=config.get("setup_name", "custom_setup"),
                        required_objects=config.get("required_objects", {}),
                        regions=regions
                    )

                    for r in config.get("spatial_rules", []):
                        spatial_rules.append(SpatialRule(
                            rule_type=r["rule_type"],
                            subject_class=r["subject_class"],
                            target=r["target"],
                            threshold=r.get("threshold")
                        ))
                except Exception as e:
                    print(f"Error loading setup config: {e}", file=sys.stderr)
                    sys.exit(1)

        pipeline = LabLensPipeline(model_path=args.model)
        result = pipeline.run(args.image, setup_spec, spatial_rules)

        if args.json:
            print(json.dumps(result.to_dict(), indent=2))
        else:
            print("LAB LENS")
            print("────────────────────────────")
            print(f"Image: {args.image}")
            print()
            print("Image Quality:")
            if result.quality:
                print(f"  {result.quality.status}")
                if result.quality.warnings:
                    for w in result.quality.warnings:
                        print(f"  - WARNING: {w}")
            else:
                print("  ERROR")
            print()
            print("Detections:")
            if result.detections:
                for d in result.detections:
                    print(f"  {d.id.ljust(14)} confidence={d.confidence:.2f}")
            else:
                print("  None")
            print()
            print("Spatial Analysis:")
            if result.compliance_result and result.compliance_result.satisfied_rules:
                for rule in result.compliance_result.satisfied_rules:
                    print(f"  {rule}")
            else:
                print("  None")
            print()
            print("Setup:")
            print(f"  {setup_spec.setup_name if setup_spec else 'UNSPECIFIED'}")
            print()
            print("Compliance:")
            print(f"  {result.compliance_status}")
            print()
            print("Violations:")
            if result.compliance_result and result.compliance_result.violations:
                for v in result.compliance_result.violations:
                    print(f"  - {v.message}")
            else:
                print("  None")
            print()
            print("Warnings/Errors:")
            for w in result.warnings:
                print(f"  - WARNING: {w}")
            if result.error:
                print(f"  - ERROR: {result.error}")
    elif args.command == "quality":
        from lab_lens.config.loader import load_config
        from lab_lens.preprocessing.image_quality import analyze_image_quality
        import cv2

        try:
            config = load_config(args.config)
            img = cv2.imread(args.input)
            if img is None:
                print(f"Error: Could not load image {args.input}")
                sys.exit(1)

            res = analyze_image_quality(img, config)
            print("LAB LENS — IMAGE QUALITY ANALYSIS\n")
            print(f"Image: {args.input}")
            print(f"Resolution: {res.width}x{res.height}")
            print(f"Brightness: {res.brightness:.2f}")
            print(f"Contrast: {res.contrast:.2f}")
            print(f"Blur: {res.blur_score:.2f}\n")
            print(f"Overall quality: {res.status}")
            print(f"Warnings: {', '.join(res.warnings) if res.warnings else 'None'}")

            if res.status == "FAIL":
                sys.exit(1)
        except Exception as e:
            print(f"Error processing image: {e}")
            sys.exit(1)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
