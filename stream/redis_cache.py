# stream/redis_cache.py
import redis, json, os
from dotenv import load_dotenv
load_dotenv()


r = redis.Redis(host=os.getenv("REDIS_HOST"), port=int(os.getenv("REDIS_PORT")), db=0)

def cache_record(key, record):
    r.set(key, json.dumps(record), ex=3600)
