"""
Compute HR@K / NDCG@K on chronological split
Milestone 3: Offline Evaluation
"""

from pathlib import Path
import pandas as pd
import numpy as np
import json
import math

# Config
DATA = Path("data/interactions.csv")  # Replace with real dataset path
OUT = Path("results/offline_eval.json")
K = 10


# ---------- Metric helpers ----------
def hit_ratio_at_k(recs, truth, k=K):
    """HR@K = 1 if any relevant item in top-K, else 0."""
    return int(len(set(recs[:k]) & truth) > 0)


def ndcg_at_k(recs, truth, k=K):
    """Normalized Discounted Cumulative Gain."""
    dcg = 0.0
    for i, iid in enumerate(recs[:k], start=1):
        if iid in truth:
            dcg += 1.0 / math.log2(i + 1)
    idcg = sum(1.0 / math.log2(i + 1) for i in range(1, min(k, len(truth)) + 1))
    return dcg / idcg if idcg else 0.0


# ---------- Evaluation ----------
def chronological_split(df, ratios=(0.7, 0.15, 0.15)):
    """Split chronologically into train/val/test."""
    df = df.sort_values("timestamp")
    n = len(df)
    a = int(n * ratios[0])
    b = int(n * (ratios[0] + ratios[1]))
    return df.iloc[:a], df.iloc[a:b], df.iloc[b:]


def popularity_baseline(train_df, k=K):
    """Recommend most-watched items as a baseline."""
    top = (
        train_df.groupby("item_id")["watched"]
        .sum()
        .sort_values(ascending=False)
        .head(k)
        .index.tolist()
    )
    return top


def evaluate(df_test, recommender_fn):
    """Evaluate HR@K and NDCG@K."""
    rows = []
    for uid, group in df_test.groupby("user_id"):
        truth = set(group.loc[group["watched"] == 1, "item_id"])
        if not truth:
            continue
        recs = recommender_fn(uid)
        rows.append(
            {"HR@10": hit_ratio_at_k(recs, truth), "NDCG@10": ndcg_at_k(recs, truth)}
        )
    return pd.DataFrame(rows).mean().to_dict()


def main():
    Path("results").mkdir(exist_ok=True)

    # Temporary dummy dataset
    df = pd.DataFrame(
        {
            "user_id": np.repeat([1, 2, 3], 3),
            "item_id": [10, 11, 12, 10, 13, 14, 11, 12, 15],
            "watched": [1, 0, 1, 1, 1, 0, 0, 1, 1],
            "timestamp": pd.date_range("2023-01-01", periods=9, freq="D"),
        }
    )

    train, val, test = chronological_split(df)
    top_items = popularity_baseline(train)

    def baseline_recommender(uid):
        return top_items

    metrics = evaluate(test, baseline_recommender)
    with open(OUT, "w") as f:
        json.dump(metrics, f, indent=2)
    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()

