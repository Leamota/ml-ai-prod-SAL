"""
Milestone 3: Online Metric Specification & Results
Joins reco_responses with watch events to compute an online KPI proxy.
"""

from pathlib import Path
import pandas as pd
import json

# Example data source (simulated Kafka topics)
RECO_LOG = Path("data/reco_responses_sample.json")
OUT = Path("results/online_eval.json")

# Parameters
TIME_WINDOW_MIN = 10  # minutes to consider a recommendation successful


def generate_sample_logs():
    """Create a small simulated log if none exists."""
    data = {
        "recommendations": [
            {"user_id": 1, "item_id": 101, "reco_ts": "2023-01-01T00:00:00"},
            {"user_id": 1, "item_id": 102, "reco_ts": "2023-01-01T00:05:00"},
            {"user_id": 2, "item_id": 103, "reco_ts": "2023-01-01T00:03:00"},
        ],
        "watch_events": [
            {"user_id": 1, "item_id": 101, "watch_ts": "2023-01-01T00:04:00"},
            {"user_id": 1, "item_id": 102, "watch_ts": "2023-01-01T00:40:00"},
            {"user_id": 2, "item_id": 103, "watch_ts": "2023-01-01T00:06:00"},
        ],
    }
    Path("data").mkdir(exist_ok=True)
    with open(RECO_LOG, "w") as f:
        json.dump(data, f, indent=2)


def compute_kpi(df_reco, df_watch, window_min=TIME_WINDOW_MIN):
    """Compute success ratio of recommendations watched within N minutes."""
    df_reco["reco_ts"] = pd.to_datetime(df_reco["reco_ts"])
    df_watch["watch_ts"] = pd.to_datetime(df_watch["watch_ts"])

    success_count = 0
    total_count = len(df_reco)

    for _, row in df_reco.iterrows():
        uid, iid, reco_time = row[["user_id", "item_id", "reco_ts"]]
        matches = df_watch[
            (df_watch["user_id"] == uid)
            & (df_watch["item_id"] == iid)
            & (
                (df_watch["watch_ts"] - reco_time)
                .dt.total_seconds()
                .between(0, window_min * 60)
            )
        ]
        if not matches.empty:
            success_count += 1

    return {"Online KPI": success_count / total_count if total_count else 0.0}


def main():
    if not RECO_LOG.exists():
        generate_sample_logs()

    with open(RECO_LOG) as f:
        logs = json.load(f)

    df_reco = pd.DataFrame(logs["recommendations"])
    df_watch = pd.DataFrame(logs["watch_events"])

    metrics = compute_kpi(df_reco, df_watch)
    Path("results").mkdir(exist_ok=True)
    with open(OUT, "w") as f:
        json.dump(metrics, f, indent=2)

    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()
