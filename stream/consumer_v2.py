


import os, json
from confluent_kafka import Consumer
from dotenv import load_dotenv
from .schemas import WatchEvent, RateEvent
from .snapshot_writer import write_snapshot
from .redis_cache import cache_record

load_dotenv()

# Kafka configuration from .env
conf = {
    'bootstrap.servers': os.getenv('KAFKA_BOOTSTRAP'),
    'security.protocol': os.getenv('KAFKA_SECURITY_PROTOCOL', 'SASL_SSL'),
    'sasl.mechanisms': os.getenv('KAFKA_SASL_MECHANISM', 'PLAIN'),
    'sasl.username': os.getenv('KAFKA_API_KEY'),
    'sasl.password': os.getenv('KAFKA_API_SECRET'),
    'group.id': os.getenv('KAFKA_GROUP_ID', 'ingestor'),
    'auto.offset.reset': 'earliest'
}

for key, value in conf.items():
    if value is None:
        raise ValueError(f"Missing Kafka config: {key}")

# Topics from .env or defaults
watch = os.getenv('WATCH_TOPIC', 'sal.watch')
rate = os.getenv('RATE_TOPIC', 'sal.rate')
topics = [watch, rate]

# Schema mapping
SCHEMA_MAP = {
    watch: WatchEvent,
    rate: RateEvent
}

def main():
    consumer = Consumer(conf)
    consumer.subscribe(topics)
    print(f" Subscribed to: {topics}")

    buffer = {}

    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None: continue
            if msg.error():
                print(f"⚠️ Kafka error: {msg.error()}"); continue

            topic = msg.topic()
            raw = msg.value().decode("utf-8")

            try:
                data = json.loads(raw)
                schema = SCHEMA_MAP.get(topic)
                if not schema:
                    print(f"⚠️ Unknown topic: {topic}"); continue

                validated = schema(**data).model_dump()

                if topic not in buffer:
                    buffer[topic] = []
                buffer[topic].append(validated)

                cache_record(f"{topic}:{validated['user_id']}", validated)

                if len(buffer[topic]) >= 100:
                    write_snapshot(topic, buffer[topic], format="parquet")
                    buffer[topic] = []
                    consumer.commit(msg)

            except Exception as e:
                print(f"⚠️ Validation error: {e}")

    finally:
        consumer.close()
        print(" Consumer closed.")

if __name__ == '__main__':
    main()