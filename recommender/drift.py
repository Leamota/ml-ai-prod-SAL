"""
Milestone 3: Data Quality & Drift Analysis
Compares latest user/movie distributions vs baseline using Wasserstein distance.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from scipy.stats import wasserstein_distance
import json

# Example baseline + current data
BASELINE_PATH = Path("data/baseline_users.csv")
CURRENT_PATH = Path("data/current_users.csv")
OUT = Path("results/drift_report.json")


def generate_sample_data():
    """Create small baseline/current samples for demonstration."""
    Path("data").mkdir(exist_ok=True)
    np.random.seed(42)
    baseline = pd.DataFrame({
        "age": np.random.normal(30, 5, 1000),
        "activity_level": np.random.normal(50, 10, 1000),
    })
    current = pd.DataFrame({
        "age": np.random.normal(33, 5, 1000),
        "activity_level": np.random.normal(48, 12, 1000),
    })
    baseline.to_csv(BASELINE_PATH, index=False)
    current.to_csv(CURRENT_PATH, index=False)


def compute_drift(baseline_df, current_df):
    """Compute Wasserstein distance per numeric column."""
    results = {}
    for col in baseline_df.columns:
        if np.issubdtype(baseline_df[col].dtype, np.number):
            dist = wasserstein_distance(baseline_df[col], current_df[col])
            results[col] = float(dist)
    return results


def main():
    if not BASELINE_PATH.exists() or not CURRENT_PATH.exists():
        generate_sample_data()

    baseline_df = pd.read_csv(BASELINE_PATH)
    current_df = pd.read_csv(CURRENT_PATH)

    drift_scores = compute_drift(baseline_df, current_df)
    Path("results").mkdir(exist_ok=True)
    with open(OUT, "w") as f:
        json.dump(drift_scores, f, indent=2)

    print(json.dumps(drift_scores, indent=2))


if __name__ == "__main__":
    main()

