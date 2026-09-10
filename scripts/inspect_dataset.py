import argparse
import yaml
from pathlib import Path

def inspect(dataset_dir: str):
    dataset_path = Path(dataset_dir)
    yaml_path = dataset_path / "data.yaml"
    
    if not yaml_path.exists():
        print("data.yaml not found.")
        return
        
    with open(yaml_path, 'r') as f:
        data = yaml.safe_load(f)
        
    print("Dataset Inspection Report")
    print("-------------------------")
    print(f"Classes (nc): {data.get('nc')}")
    print(f"Names: {data.get('names')}")
    
    # We could calculate the actual instances per class from validate_dataset, 
    # but for simplicity of this script we will just list the config for now.

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset', required=True)
    args = parser.parse_args()
    inspect(args.dataset)
