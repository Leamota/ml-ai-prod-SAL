from fastapi import FastAPI
import random

app = FastAPI()

@app.get("/healthz")
def healthz():
    return {"status": "ok", "version": "v0.2"}

@app.get("/recommend/{user_id}")
def recommend(user_id: int, k: int = 5):
    # Placeholder recommendations (replace with real model output later)
    recommended_movies = random.sample(range(1, 100), k)
    return {"user_id": user_id, "recommendations": recommended_movies}

@app.get("/metrics")
def metrics():
    # Simple metrics output for now
    return {"precision@5": 0.32, "recall@5": 0.45}
