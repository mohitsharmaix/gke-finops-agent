def compute_metrics(w):
    cpu_util = w["cpu_usage"] / w["cpu_request"] if w["cpu_request"] else 0
    mem_util = w["memory_usage"] / w["memory_request"] if w["memory_request"] else 0

    w["cpu_utilization"] = cpu_util
    w["memory_utilization"] = mem_util

    w["cpu_waste"] = 1 - cpu_util if cpu_util < 1 else 0
    w["memory_waste"] = 1 - mem_util if mem_util < 1 else 0

    return w


def generate_recommendation(w):
    rec = []

    if w["cpu_utilization"] < 0.3:
        rec.append(f"Reduce CPU request by ~50%")

    if w["cpu_utilization"] > 0.8:
        rec.append("Increase CPU request (risk of throttling)")

    if w["memory_utilization"] < 0.4:
        rec.append("Reduce memory request")

    if w["memory_utilization"] > 0.85:
        rec.append("Increase memory (OOM risk)")

    return rec