import os, time, requests, random, json
from datetime import datetime

TEAM = os.getenv("TEAM", "sal")
API = os.getenv("RECO_API", "http://localhost:8080")
REQUEST_DIR = f"{TEAM}.reco_requests"
RESPONSE_DIR = f"{TEAM}.reco_responses"

os.makedirs(REQUEST_DIR, exist_ok=True)
os.makedirs(RESPONSE_DIR, exist_ok=True)

def main():
    user = random.randint(1, 1000)
    timestamp = datetime.utcnow().isoformat()
    request_path = f"{REQUEST_DIR}/{timestamp}_{user}.json"
    response_path = f"{RESPONSE_DIR}/{timestamp}_{user}.json"

    try:
        r = requests.get(f"{API}/recommend/{user}", timeout=5)
        req_data = {"user_id": user, "timestamp": timestamp}
        res_data = {"status": r.status_code, "body": r.text, "timestamp": timestamp}

        with open(request_path, "w") as f:
            json.dump(req_data, f)
        with open(response_path, "w") as f:
            json.dump(res_data, f)

        print(" Probe success:", res_data)
    except Exception as e:
        print("❌ Probe error:", e)

if __name__ == '__main__':
    main()
