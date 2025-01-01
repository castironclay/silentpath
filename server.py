import base64
import multiprocessing
import os
import time

import boto3
import netifaces
from netfilterqueue import NetfilterQueue
from scapy.all import IP, Ether, raw, sendp
import zstd

sqs = boto3.client(
    "sqs",
    region_name="us-east-1",
    aws_access_key_id=os.environ["AWS_ACCESS_KEY"],
    aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
    use_ssl=True,
)

queue_url = f'https://sqs.us-east-1.amazonaws.com/{os.environ["ACCOUNT_ID"]}/{os.environ["PROJECT_NAME"]}_server'
addrs = netifaces.ifaddresses("wlan0")
mac = addrs[netifaces.AF_LINK][0]["addr"]


def process_received_packet(compressed_packet):
    global mac
    # Decode the Base64 back into bytes
    decompressed = zstd.decompress(compressed_packet)
    raw_packet = base64.b64decode(decompressed).encode()
    packet = IP(raw_packet)
    print(f"Recreated Packet: {packet.summary()}")
    # Local MAC address
    sendp(Ether(dst=mac) / packet)  # Send the packet at layer2


# Function to process each message
def process_message(message):
    print(f"Processing message: {message['Body']}")
    data = message["Body"]
    print(data)
    if data:
        process_received_packet(data)


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


def send_sqs(data) -> None:
    response = sqs.send_message(
        QueueUrl=os.environ["CLIENT_QUEUE_URL"],
        MessageBody=data,
    )
    print(response)

def process_packet(packet):
    # Grab payload
    scapy_packet = IP(packet.get_payload())
    # Encode as base64 bytestring
    encoded_packet = base64.b64encode(raw(scapy_packet))
    # Compress bytestring
    compressed = zstd.compress(encoded_packet) 
    # Send decoded bytestring (SQS limitation)
    send_sqs(encoded_packet.decode())
    packet.drop()

def run_nfqueue():
    try:
        nfqueue = NetfilterQueue()
        nfqueue.bind(1, process_packet)
        print("Listening for packets...")
        nfqueue.run()

    except KeyboardInterrupt:
        print("Stopping...")
        nfqueue.unbind()


if __name__ == "__main__":
    print("Starting server..")
    p1 = multiprocessing.Process(target=listen_for_messages)
    p2 = multiprocessing.Process(target=run_nfqueue)

    p1.start()
    p2.start()

    p1.join()
    p2.join()
