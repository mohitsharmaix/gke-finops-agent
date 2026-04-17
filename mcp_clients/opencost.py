import requests
import yaml

with open("config.yaml") as f:
    config = yaml.safe_load(f)

BASE_URL = config["opencost"]["base_url"]

def get_cost_allocation():
    url = f"{BASE_URL}/allocation"
    return requests.get(url).json()

def get_idle_cost():
    url = f"{BASE_URL}/idle"
    return requests.get(url).json()