import os
from typing import Dict, List

def load_config(file_path: str = "config.properties") -> Dict:
    config = {}
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Config file not found: {file_path}")
    
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                if '=' in line:
                    key, value = line.split('=', 1)
                    config[key.strip()] = value.strip()
    
    return config

def get_urls(config: Dict) -> List[str]:
    urls_str = config.get('URLS', '')
    return [url.strip() for url in urls_str.split(',') if url.strip()]

def get_request_delay(config: Dict) -> float:
    try:
        return float(config.get('REQUEST_DELAY', 2))
    except:
        return 2.0
