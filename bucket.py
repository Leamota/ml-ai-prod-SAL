import boto3
import os

# Load environment variables manually or use dotenv
os.environ["AWS_ACCESS_KEY_ID"] = "test"
os.environ["AWS_SECRET_ACCESS_KEY"] = "test"
os.environ["AWS_REGION"] = "us-east-1"
os.environ["S3_ENDPOINT"] = "http://localhost:4566"
os.environ["S3_BUCKET"] = "sal-snapshots"

# Create S3 client
s3 = boto3.client(
    "s3",
    endpoint_url=os.getenv("S3_ENDPOINT"),
    region_name=os.getenv("AWS_REGION"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
)

# Create bucket
s3.create_bucket(Bucket=os.getenv("S3_BUCKET"))
print("Bucket created successfully.")
