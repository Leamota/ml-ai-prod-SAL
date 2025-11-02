# stream/snapshot_writer.py
import pandas as pd, io, boto3, os

def write_snapshot(topic, records, format="parquet", s3_client=None):
    if not records:
        return

    if isinstance(records, dict):
        records = [records]

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
    else:
        raise ValueError(f"Unsupported format: {format}")

    buffer.seek(0)
    s3_client = s3_client or boto3.client("s3")
    s3_client.upload_fileobj(buffer, os.getenv("S3_BUCKET"), key)

