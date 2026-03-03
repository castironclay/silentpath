import discord
import base64
import netifaces
import threading
from netfilterqueue import NetfilterQueue
from scapy.all import IP, Ether, raw, sendp
import zstd
import asyncio

addrs = netifaces.ifaddresses("wlan0")
mac = addrs[netifaces.AF_LINK][0]["addr"]

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        # Only worry about messages from the peer
        print(message.author.id)
        if message.author.id == BOT_AUTHOR_ID:
            compressed_packet = message.content
            global mac
            # Decode the Base64 back into bytes
            packet = bytes.fromhex(compressed_packet)
            decompressed = zstd.decompress(packet)
            raw_packet = base64.b64decode(decompressed)
            packet = IP(raw_packet)
            # Local MAC address
            sendp(Ether(dst=mac) / packet)  # Send the packet at layer2

def process_message(message):
    print(f"Processing message: {message['Body']}")
    data = message["Body"]
    if data:
        process_received_packet(data)

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)

def start_client(client: discord.Client, stop_event: threading.Event) -> None:
    try:
        client.run('TOKEN')

    except KeyboardInterrupt:
        print("Stopping Discord...")

    finally:
        stop_event.set()          

def process_packet(packet):
    scapy_packet = IP(packet.get_payload())
    encoded_packet = base64.b64encode(raw(scapy_packet))
    compressed = zstd.compress(encoded_packet)
    #send_sqs(compressed.hex())

    future = asyncio.run_coroutine_threadsafe(
        send_text('CHANNEL', compressed.hex()),   # the coroutine we want to run
        client.loop                    # the event loop that the client owns
    )

    packet.drop()

def run_nfqueue(stop_event: threading.Event):
    try:
        nfqueue = NetfilterQueue()
        nfqueue.bind(1, process_packet)
        print("Listening for packets...")
        nfqueue.run()

    except KeyboardInterrupt:
        print("Stopping NFQueue...")

    finally:
        stop_event.set()          # Signal the other thread to stop
        nfqueue.unbind()


## Message
async def send_text(channel_id: int, text: str):
    """Coroutine that fetches the channel and sends `text`."""
    channel = client.get_channel(channel_id)
    if channel is None:
        # If the channel isn’t cached yet, fetch it from the API
        channel = await client.fetch_channel(channel_id)

    await channel.send(text)
    print(f"📤 Sent: {text}")

if __name__ == "__main__":
    print("Starting client..")
    stop_event = threading.Event()

    # Create the two worker threads
    t1 = threading.Thread(target=start_client, args=(client, stop_event,), name="Discord")
    t2 = threading.Thread(target=run_nfqueue, args=(stop_event,), name="NfQueue")

    t1.start()
    t2.start()

    try:
        t1.join()
        t2.join()
    except KeyboardInterrupt:
        print("\nKeyboard interrupt received – shutting down...")
        stop_event.set()
        t1.join()
        t2.join()
