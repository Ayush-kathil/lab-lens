import argparse
import yaml
from pathlib import Path

def inspect(dataset_dir: str):
    dataset_path = Path(dataset_dir)
    data_yaml_paths = list(dataset_path.rglob("data.yaml"))
    if not data_yaml_paths:
        print("data.yaml not found.")
        return
        
    data_yaml_path = data_yaml_paths[0]
    with open(data_yaml_path, 'r', encoding='utf-8') as f:
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
