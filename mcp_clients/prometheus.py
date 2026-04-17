import requests
import yaml

with open("config.yaml") as f:
    config = yaml.safe_load(f)

BASE_URL = config["prometheus"]["base_url"]

def query_prometheus(query):
    url = f"{BASE_URL}/query"
    resp = requests.get(url, params={"query": query})
    return resp.json()

def get_cpu_usage():
    query = 'sum(rate(container_cpu_usage_seconds_total{container!="",pod!=""}[5m])) by (pod, namespace)'
    return query_prometheus(query)

def get_memory_usage():
    query = 'container_memory_working_set_bytes{container!="",pod!=""}'
    return query_prometheus(query)