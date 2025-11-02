Goal: “To evaluate model recommendations using historical user–item interactions.”

Dataset: Describe what data you’re using (e.g., movie ratings, clicks, etc.).

Split: Chronological (train before test to prevent leakage).

Metrics: Choose 2–3 metrics such as Precision@10, Recall@10, MAP, NDCG.

Evaluation Procedure: Describe how predictions are ranked and compared.

Output: Results stored in results/offline_eval.json.

📎 Code: scripts/offline_eval.py  
📎 Config: config/eval_config.yaml
