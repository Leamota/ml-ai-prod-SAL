import matplotlib.pyplot as plt


def plot_drift(old_counts, new_counts):
    plt.bar(old_counts.index - 0.2, old_counts.values, width=0.4, label="Old Data")
    plt.bar(new_counts.index + 0.2, new_counts.values, width=0.4, label="New Data")
    plt.xlabel("Rating")
    plt.ylabel("Count")
    plt.legend()
    plt.title("Rating Distribution Drift")
    plt.savefig("docs/drift_chart.png")
