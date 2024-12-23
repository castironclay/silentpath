import os
import time

import boto3

sqs = boto3.client(
    "sqs",
    region_name="us-east-1",
    aws_access_key_id=os.environ["AWS_ACCESS_KEY"],
    aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
    use_ssl=True,
)

queue_url = f'https://sqs.us-east-1.amazonaws.com/{os.environ["ACCOUNT_ID"]}/{os.environ["PROJECT_NAME"]}_client'


# Function to process each message
def process_message(message):
    # Placeholder for your message processing logic
    print(f"Processing message: {message['Body']}")


def listen_for_messages():
    while True:
        try:
            response = sqs.receive_message(
                QueueUrl=queue_url,
                MaxNumberOfMessages=1,
                WaitTimeSeconds=20,
                VisibilityTimeout=30,
            )

            # Check if there are any messages
            messages = response.get("Messages", [])
            if messages:
                for message in messages:
                    process_message(message)

                    # Delete the message
                    receipt_handle = message["ReceiptHandle"]
                    sqs.delete_message(QueueUrl=queue_url, ReceiptHandle=receipt_handle)
                    print(f"Message deleted: {receipt_handle}")
            else:
                print("No messages received. Waiting...")

        except Exception as e:
            print(f"An error occurred: {e}")

        time.sleep(0.25)


# Start listening for messages
if __name__ == "__main__":
    print("Starting client listener")
    listen_for_messages()
