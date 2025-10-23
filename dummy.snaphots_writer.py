import pandas as pd, io, boto3, os

s3 = boto3.client(
    "s3",
    endpoint_url=os.getenv("S3_ENDPOINT"),
    region_name=os.getenv("AWS_REGION"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
)

def write_snapshot(topic, records):
    if not records: return
    df = pd.DataFrame(records)
    buffer = io.BytesIO()
    df.to_parquet(buffer, index=False)
    key = f"snapshots/{topic}/snapshot_{pd.Timestamp.now().isoformat()}.parquet"
    buffer.seek(0)
    s3.upload_fileobj(buffer, os.getenv("S3_BUCKET"), key)
