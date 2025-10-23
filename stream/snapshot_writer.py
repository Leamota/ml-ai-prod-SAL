# stream/snapshot_writer.py
import pandas as pd, io, boto3, os

s3 = boto3.client("s3")

def write_snapshot(topic, records):
    if not records: return
    df = pd.DataFrame(records)
    buffer = io.BytesIO()
    df.to_parquet(buffer, index=False)
    key = f"{os.getenv('S3_PREFIX','snapshots/')}{topic}/{pd.Timestamp.now().isoformat()}.parquet"
    buffer.seek(0)
    s3.upload_fileobj(buffer, os.getenv("S3_BUCKET"), key)



