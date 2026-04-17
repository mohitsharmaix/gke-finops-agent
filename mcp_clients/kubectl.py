import requests
import yaml

with open("config.yaml") as f:
    config = yaml.safe_load(f)

BASE_URL = config["kubectl"]["base_url"]

def get_pods():
    url = f"{BASE_URL}/kubectl"
    payload = {"command": "get pods -A -o json"}
    return requests.post(url, json=payload).json()