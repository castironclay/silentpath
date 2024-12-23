import os

import boto3

project_name = os.environ["PROJECT_NAME"]
region = "us-east-1"

sqs_client = boto3.client(
    "sqs",
    region_name=region,
    aws_access_key_id=os.environ["AWS_ACCESS_KEY"],
    aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
    use_ssl=True,
)

# Create SQS queue: server
sqs_client.create_queue(
    QueueName=f"{project_name}_server",
    Attributes={"ReceiveMessageWaitTimeSeconds": "20"},
)

# Create SQS queue: client
sqs_client.create_queue(
    QueueName=f"{project_name}_client",
    Attributes={"ReceiveMessageWaitTimeSeconds": "20"},
)
