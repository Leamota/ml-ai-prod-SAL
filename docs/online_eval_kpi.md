## 1. Goal
Define a measurable **online performance metric (KPI)** that evaluates how effectively our recommender system engages users in real-time production conditions.

Unlike offline metrics (Precision@K, Recall@K, etc.), this KPI is based on **live behavioral signals** collected from Kafka event streams.

---

## 2. Data Source
- **Kafka Topic:** `{team}.reco_responses`  
- **Event Types:**
  - `recommendation_sent` — system output when recommendations are served
  - `user_click` — user clicks on a recommended item
  - `user_watch` — user begins watching the recommended item
- **Timestamps:** All events include UTC timestamps to allow window-based matching.
- **Identifiers:**
  - `user_id`
  - `item_id`
  - `session_id`
  - `recommendation_id`

---

## 3. Proxy Success Definition
A recommendation is considered **successful** if the user **interacts with or watches** at least one recommended title within **N minutes** of receiving it.

For our baseline:
- **N = 10 minutes**
- A “watch event” is defined as any `user_watch` event associated with the same `recommendation_id` as the recommendation event.

This proxy metric approximates user satisfaction and engagement with the recommendation feed.

---

## 4. KPI Computation Method

**Formula:**

**KPI = (Number of Successful Recommendations) ÷ (Total Recommendations Sent)**


Where:
- Successful recommendations = Recommendations that led to a `user_watch` event within 10 minutes  
- Total recommendations = All `recommendation_sent` events during the evaluation window

### Pseudocode
```python
# Pseudocode outline for KPI computation
# Source: scripts/online_eval.py

# 1. Read events from Kafka topic
events = read_kafka_topic("{team}.reco_responses")

# 2. Filter and join events
recommendations = events[events["event_type"] == "recommendation_sent"]
watches = events[events["event_type"] == "user_watch"]

# 3. Join on recommendation_id and time window ≤ N minutes
joined = recommendations.merge(watches, on="recommendation_id")
joined["time_diff"] = joined["timestamp_watch"] - joined["timestamp_sent"]
successful = joined[joined["time_diff"] <= pd.Timedelta(minutes=10)]

# 4. Compute KPI
kpi_value = len(successful) / len(recommendations)
print(f"Online KPI = {kpi_value:.3f}")
