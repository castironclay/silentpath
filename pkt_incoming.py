from netfilterqueue import NetfilterQueue
from scapy.all import IP, sendp, Ether
import base64
import socket

def process_received_packet(base64_packet):
    # Decode the Base64 back into bytes
    raw_packet = base64.b64decode(base64_packet)
    packet = IP(raw_packet)
    print(f"Recreated Packet: {packet.summary()}")
    # Receiving NIC MAC address
    sendp(Ether(dst="2c:cf:67:51:c5:66") / packet)  # Send the packet at layer2

def start_server():
    HOST = ''  # Listen on all interfaces
    PORT = 22222
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print("Server listening...")
        while True:
            conn, addr = s.accept()
            with conn:
                data = conn.recv(4096)
                if data:
                    process_received_packet(data.decode())

start_server()