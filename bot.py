import os
import discord

# Credentials
DISCORD_TOKEN = os.environ.get('DISCORD_TOKEN')
CHANNEL_ID = 1251180886284701767

# Initialize the bot
intents = discord.Intents.default()
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print("Bot is ready.")
    channel = client.get_channel(CHANNEL_ID)
    if channel:
        print(f"Channel found: {channel.name}")
        await channel.send(f"We have logged in as {client.user}")
    else:
        print("Channel not found.")
    
# Function to send a message to the specified Discord channel
async def send_win_message(player_name, win):
    channel = client.get_channel(CHANNEL_ID)
    if win:
        await channel.send(f"{player_name} has just finished a game and won!")
    else:
        await channel.send(f"{player_name} has just finished a game and lost!")


if DISCORD_TOKEN:    
    client.run(DISCORD_TOKEN)
else:
    print(f"Invalid bot api token: {DISCORD_TOKEN}")