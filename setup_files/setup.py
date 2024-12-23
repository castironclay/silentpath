import json
import os

import boto3

project_name = os.environ["PROJECT_NAME"]
account_id = os.environ["ACCOUNT_ID"]
region = "us-east-1"

events_client = boto3.client(
    "events",
    region_name=region,
    aws_access_key_id=os.environ["AWS_ACCESS_KEY"],
    aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
    use_ssl=True,
)

# Define the event pattern (e.g., S3 object uploaded)
event_pattern = {
    "source": ["aws.s3"],
    "resources": [f"arn:aws:s3:::{project_name}"],
    "detail-type": ["AWS API Call via CloudTrail"],
    "detail": {"eventName": ["PutObject", "UploadPart", "CompleteMultipartUpload"]},
}

# Create a rule with the specified event pattern

response = events_client.put_rule(
    Name=f"{project_name}_rule",
    EventPattern=json.dumps(event_pattern),
    State="ENABLED",
    Description=f"S3 uploads to {project_name} bucket",
)

# Create SQS queue
sqs_client = boto3.client(
    "sqs",
    region_name=region,
    aws_access_key_id=os.environ["AWS_ACCESS_KEY"],
    aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
    use_ssl=True,
)
response = sqs_client.create_queue(
    QueueName=f"{project_name}_listener",
)
queue_arn = f"arn:aws:sqs:{region}:{account_id}:{project_name}_listener"
# Add the SQS queue as a target to the EventBridge rule
events_client.put_targets(
    Rule=f"{project_name}_rule", Targets=[{"Arn": queue_arn, "Id": "sqs-target"}]
)
