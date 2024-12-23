import os

import boto3

s3_client = boto3.client(
    "s3",
    region_name="us-east-1",
    aws_access_key_id=os.environ["AWS_ACCESS_KEY"],
    aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
    use_ssl=True,
)

s3_client.download_file("silentpath", "test_file.txt", "new_file.txt")
