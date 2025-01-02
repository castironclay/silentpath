import discord
from discord.ext import commands
from netfilterqueue import NetfilterQueue
from scapy.all import IP, Ether, raw, sendp
import zstd
import multiprocessing
import base64
import os

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

client = discord.Client(intents=intents)


def process_packet(packet):
    global client
    scapy_packet = IP(packet.get_payload())
    encoded_packet = base64.b64encode(raw(scapy_packet))
    compressed = zstd.compress(encoded_packet) 
    channel = client.get_channel(1324114022223843449)    
    print(channel)
    channel.send(compressed.hex())
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

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    print(message)
    print(message.content)
    print(message.channel)
    channel = client.get_channel(1324114022223843449)    
    if message.content == "asdf":
        await channel.send('Hello, world!')

    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

def start():
    client.run(os.environ["BOT_TOKEN"])

if __name__ == "__main__":
    print("Starting server..")
    p1 = multiprocessing.Process(target=start)
    p2 = multiprocessing.Process(target=run_nfqueue)

    p1.start()
    p2.start()

    p1.join()
    p2.join()
