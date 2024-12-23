import os

import boto3

client = boto3.client(
    "sqs",
    region_name="us-east-1",
    aws_access_key_id=os.environ["AWS_ACCESS_KEY"],
    aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
    use_ssl=True,
)

client.send_message(
    QueueUrl=os.environ["CLIENT_QUEUE_URL"],
    MessageBody="string",
)
