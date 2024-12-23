import os

import boto3
from botocore.exceptions import ClientError
from loguru import logger

s3_client = boto3.client(
    "s3",
    region_name="us-east-1",
    aws_access_key_id=os.environ["AWS_ACCESS_KEY"],
    aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
    use_ssl=True,
)


def download_file(file_name, bucket, object_name=None):
    global s3_client
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file
    try:
        s3_client.download_file(file_name, bucket, object_name)
    except ClientError as e:
        logger.error(e)
        return False
    return True


download_file("silentpath", "test_file.txt", "new_file.txt")
