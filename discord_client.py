import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

client = discord.Client(intents=intents)

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

client.run(os.environ["BOT_TOKEN"])