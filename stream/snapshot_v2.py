import pandas as pd, io, boto3, os

s3 = boto3.client("s3")

def write_snapshot(topic, records, format="parquet"):
    if not records: return

    df = pd.DataFrame(records)
    buffer = io.BytesIO()

    timestamp = pd.Timestamp.now().strftime("%Y%m%d-%H%M%S")
    key = f"{os.getenv('S3_PREFIX','snapshots/')}{topic}/{timestamp}.{format}"

    if format == "parquet":
        df.to_parquet(buffer, index=False)
    elif format == "csv":
        buffer = io.StringIO()
        df.to_csv(buffer, index=False)
        buffer = io.BytesIO(buffer.getvalue().encode())

    buffer.seek(0)
    s3.upload_fileobj(buffer, os.getenv("S3_BUCKET"), key)