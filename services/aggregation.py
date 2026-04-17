from mcp_clients import prometheus, kubectl, opencost
from services.normalization import parse_k8s_cpu, parse_k8s_memory

def aggregate_data():
    cpu_data = prometheus.get_cpu_usage()
    mem_data = prometheus.get_memory_usage()
    pod_data = kubectl.get_pods()
    cost_data = opencost.get_cost_allocation()

    workloads = {}

    # Parse pod specs
    for item in pod_data["items"]:
        ns = item["metadata"]["namespace"]
        pod = item["metadata"]["name"]

        for c in item["spec"]["containers"]:
            req = c.get("resources", {}).get("requests", {})

            cpu = parse_k8s_cpu(req.get("cpu", "0"))
            mem = parse_k8s_memory(req.get("memory", "0"))

            workloads[(ns, pod)] = {
                "namespace": ns,
                "pod": pod,
                "cpu_request": cpu,
                "memory_request": mem,
                "cpu_usage": 0,
                "memory_usage": 0,
                "cost": 0
            }

    # Merge CPU usage
    for result in cpu_data["data"]["result"]:
        ns = result["metric"].get("namespace")
        pod = result["metric"].get("pod")

        key = (ns, pod)
        if key in workloads:
            workloads[key]["cpu_usage"] = float(result["value"][1])

    # Merge Memory usage
    for result in mem_data["data"]["result"]:
        ns = result["metric"].get("namespace")
        pod = result["metric"].get("pod")

        key = (ns, pod)
        if key in workloads:
            workloads[key]["memory_usage"] = float(result["value"][1]) / (1024**3)

    # Merge cost (simplified)
    for entry in cost_data.get("data", []):
        ns = entry.get("namespace")
        cost = entry.get("cost", 0)

        for key in workloads:
            if key[0] == ns:
                workloads[key]["cost"] += cost

    return list(workloads.values())