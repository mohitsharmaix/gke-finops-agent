from fastapi import FastAPI
from services.aggregation import aggregate_data
from services.recommendation import compute_metrics, generate_recommendation

app = FastAPI()

@app.get("/workloads/efficiency")
def workload_efficiency():
    data = aggregate_data()
    output = []

    for w in data:
        w = compute_metrics(w)
        output.append(w)

    return output


@app.get("/cost/optimization")
def cost_optimization():
    data = aggregate_data()
    output = []

    for w in data:
        w = compute_metrics(w)
        rec = generate_recommendation(w)

        output.append({
            **w,
            "recommendations": rec
        })

    return sorted(output, key=lambda x: x["cost"], reverse=True)


@app.get("/health")
def health():
    return {"status": "ok"}