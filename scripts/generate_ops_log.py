import os, json
from datetime import datetime, timedelta

TEAM = os.getenv("TEAM", "sal")
RESPONSE_DIR = f"{TEAM}.reco_responses"
now = datetime.utcnow()
cutoff = now - timedelta(days=1)

total = 0
personalized = 0

for fname in os.listdir(RESPONSE_DIR):
    fpath = os.path.join(RESPONSE_DIR, fname)
    with open(fpath) as f:
        data = json.load(f)
        ts = datetime.fromisoformat(data["timestamp"])
        if ts >= cutoff:
            total += 1
            body = data.get("body", "")
            if "," in body or len(body.split(",")) > 1:
                personalized += 1

percent = (personalized / total * 100) if total else 0
print(f"📝 Ops Log: {total} probes in last 24h, {percent:.1f}% personalized responses")
