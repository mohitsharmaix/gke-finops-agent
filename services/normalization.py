def parse_k8s_cpu(cpu):
    if cpu.endswith("m"):
        return float(cpu.replace("m", "")) / 1000
    return float(cpu)

def parse_k8s_memory(mem):
    if mem.endswith("Mi"):
        return float(mem.replace("Mi", "")) / 1024
    if mem.endswith("Gi"):
        return float(mem.replace("Gi", ""))
    return float(mem)