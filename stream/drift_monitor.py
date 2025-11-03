import pandas as pd
from scipy.stats import entropy

def kl_divergence(p, q):
    p = p / p.sum()
    q = q / q.sum()
    return entropy(p, q)

# Example: compare rating distributions between two snapshots
df_old = pd.read_csv("data/snapshot_old.csv")
df_new = pd.read_csv("data/snapshot_new.csv")

p = df_old['rating'].value_counts().sort_index()
q = df_new['rating'].value_counts().sort_index()

drift_score = kl_divergence(p, q)
print(f"Drift Score (KL Divergence): {drift_score:.4f}")
