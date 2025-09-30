from fastapi import FastAPI, HTTPException
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import os

app = FastAPI()
reqs = Counter('recommend_requests_total','requests',['status'])
lat = Histogram('recommend_latency_seconds','latency')

@app.get('/healthz')
def healthz():
    return {"status":"ok","version":os.getenv('MODEL_VERSION','v0.1')}

@app.get('/recommend/{user_id}')
@lat.time()
def recommend(user_id: int, k: int = 20, model: str | None = None):
    try:
        ids = [50, 172, 1][:k]  # TODO: replace with real inference
        reqs.labels('200').inc()
        return ','.join(map(str, ids))
    except Exception as e:
        reqs.labels('500').inc()
        raise HTTPException(500, str(e))

@app.get('/metrics')
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}