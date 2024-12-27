import base64
import os

import boto3
from netfilterqueue import NetfilterQueue
from scapy.all import IP, raw

client = boto3.client(
    "sqs",
    region_name="us-east-1",
    aws_access_key_id=os.environ["AWS_ACCESS_KEY"],
    aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
    use_ssl=True,
)


def send_sqs(data) -> None:
    global client
    response = client.send_message(
        QueueUrl=os.environ["CLIENT_QUEUE_URL"],
        MessageBody=data,
    )
    print(response)


def process_packet(packet):
    scapy_packet = IP(packet.get_payload())
    # Convert the packet to Base64
    encoded_packet = base64.b64encode(raw(scapy_packet)).decode()
    print("Sending")
    send_sqs(encoded_packet)
    packet.drop()


nfqueue = NetfilterQueue()
nfqueue.bind(1, process_packet)

try:
    print("Listening for packets...")
    nfqueue.run()
except KeyboardInterrupt:
    print("Stopping...")
    nfqueue.unbind()
