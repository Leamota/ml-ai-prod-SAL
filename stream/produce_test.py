from confluent_kafka import Producer
from datetime import datetime
from dotenv import load_dotenv
import json
import os

load_dotenv()  # ✅ moved below all imports

conf = {
    'bootstrap.servers': 'pkc-921jm.us-east-2.aws.confluent.cloud:9092',
    'security.protocol': 'SASL_SSL',
    'sasl.mechanisms': 'PLAIN',
    'sasl.username': os.getenv('KAFKA_API_KEY'),
    'sasl.password': os.getenv('KAFKA_API_SECRET'),
}

p = Producer(conf)

def delivery_report(err, msg):
    if err is not None:
        print(f"Delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")

payload = {
    "user_id": "test123",
    "item_id": "item456",
    "timestamp": datetime.utcnow().isoformat()
}

print("Sending payload:", json.dumps(payload))

p.produce('sal.watch', key='test123', value=json.dumps(payload), callback=delivery_report)
p.flush()
