from netfilterqueue import NetfilterQueue
from scapy.all import IP, ICMP, raw, TCP
import base64
import socket

def send_to_remote(base64_packet):
    # Replace with the actual address and port of Machine B
    HOST = '192.168.86.250'
    PORT = 11111
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(base64_packet.encode())

def process_packet(packet):
    scapy_packet = IP(packet.get_payload())
    if ICMP in scapy_packet:
        # Convert the packet to Base64
        encoded_packet = base64.b64encode(raw(scapy_packet)).decode()
        send_to_remote(encoded_packet)
        print(f"Sent Base64 Packet: {encoded_packet}")
    packet.drop()  # Let the packet pass

nfqueue = NetfilterQueue()
nfqueue.bind(1, process_packet)

try:
    print("Listening for packets...")
    nfqueue.run()
except KeyboardInterrupt:
    print("Stopping...")
    nfqueue.unbind()
