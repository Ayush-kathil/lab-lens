import yaml
from pathlib import Path
from dataclasses import dataclass
from typing import Dict, Any

class ConfigurationError(Exception):
    pass

@dataclass
class AppConfig:
    dataset_path: str
    confidence_threshold: float
    image_size: int
    logging_level: str
    
def load_config(path: str) -> Dict[str, Any]:
    config_path = Path(path)
    if not config_path.exists():
        raise ConfigurationError(f"Configuration file not found: {path}")
        
    try:
        with open(config_path, 'r') as f:
            data = yaml.safe_load(f)
            if data is None:
                raise ConfigurationError(f"Configuration file is empty: {path}")
            return data
    except yaml.YAMLError as e:
        raise ConfigurationError(f"Invalid YAML in configuration: {e}")
