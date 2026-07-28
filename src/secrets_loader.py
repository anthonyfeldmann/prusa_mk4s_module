import json
from pathlib import Path

def get_secrets() -> dict:
    """Loads API keys and IPs from the secrets/prusa_secrets.json file."""
    current_dir = Path(__file__).parent
    secrets_path = current_dir / "secrets" / "prusa_secrets.json"
    
    if not secrets_path.exists():
        print(f"WARNING: Secrets file not found at {secrets_path}")
        return {}
        
    try:
        with open(secrets_path, "r") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"ERROR: Failed to parse secrets JSON: {e}")
        return {}
