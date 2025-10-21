import requests, time, random

API_URL = "http://localhost:8080"  # Replace with your live URL later

while True:
    user_id = random.randint(1, 100)
    res = requests.get(f"{API_URL}/recommend/{user_id}")
    print(f"Probe for user {user_id}: {res.status_code} - {res.json()}")
    time.sleep(60)  # every 1 minute
