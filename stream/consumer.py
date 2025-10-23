import os, time
from confluent_kafka import Consumer
from dotenv import load_dotenv
load_dotenv()
from .snapshot_writer import write_snapshot
from .redis_cache import cache_record
import json


conf = {
  'bootstrap.servers': os.getenv('KAFKA_BOOTSTRAP'),
  'security.protocol': os.getenv('KAFKA_SECURITY_PROTOCOL','SASL_SSL'),
  'sasl.mechanisms': os.getenv('KAFKA_SASL_MECHANISM','PLAIN'),
  'sasl.username': os.getenv('KAFKA_API_KEY'),
  'sasl.password': os.getenv('KAFKA_API_SECRET'),
  'group.id': os.getenv('KAFKA_GROUP','ingestor'),
  'auto.offset.reset': 'earliest'
}

def main():
    watch = os.environ.get('WATCH_TOPIC','sal.watch')
    rate = os.environ.get('RATE_TOPIC','sal.rate')
    topics = [watch, rate]
    c = Consumer(conf)
    c.subscribe(topics)
    print(f"Subscribed to: {topics}")
    try:
        while True:
            msg = c.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                print(f"Err: {msg.error()}"); continue
            # TODO: validate schema → write parquet/csv to object storage
            print(msg.topic(), msg.value()[:120])
            c.commit(msg)
    finally:
        c.close()

if __name__ == '__main__':
    main()