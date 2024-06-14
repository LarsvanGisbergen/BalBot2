import os
import discord
import json
from logic import add_score, get_users_info, get_players_info

DISCORD_TOKEN = os.environ.get('DISCORD_TOKEN')
CHANNEL_ID = 1251180886284701767

intents = discord.Intents.default()
client = discord.Client(intents=intents)

active_votes = {}  # Dictionary to store active vote message IDs mapped to game IDs
user_votes = {}  # {user_id: {game_id: vote_message_id}}

@client.event
async def on_ready():
    print("Bot is ready.")
    channel = client.get_channel(CHANNEL_ID)
    if channel:
        print(f"Channel found: {channel.name}")
        await channel.send(f"We have logged in as {client.user}")
    else:
        print("Channel not found.")

async def send_vote_message(game_id, game_name):
    channel = client.get_channel(CHANNEL_ID)
    if channel:
        message_content = f"Vote on the outcome of Game ID: {game_id}\n\nReact with 💙 if you think {game_name} will win, and ❤️ if you think {game_name} will lose!"
        vote_message = await channel.send(message_content)
        active_votes[vote_message.id] = game_id
        await vote_message.add_reaction('💙')
        await vote_message.add_reaction('❤️')
        print(f"Vote message sent for Game ID: {game_id}")

@client.event
async def on_reaction_add(reaction, user):
    if reaction.message.id in active_votes:
        game_id = active_votes[reaction.message.id]
        if str(reaction.emoji) == '💙':
            vote = "win"
        elif str(reaction.emoji) == '❤️':
            vote = "lose"
        else:
            return

        user_votes[user.id] = {"game_id": game_id, "vote": vote, "vote_message_id": reaction.message.id}
        print(f"{user.id} has voted")

@client.event
async def on_reaction_remove(reaction, user):
    if reaction.message.id in active_votes:
        await reaction.message.add_reaction(reaction.emoji)

async def update_scores(game_id, win):
    score_updates = []
    for user_id, votes in list(user_votes.items()):
        if votes["game_id"] == game_id:
            if (votes["vote"] == "win" and win) or (votes["vote"] == "lose" and not win):
                add_score(user_id, 50)
                score_updates.append(f"User {user_id} gained 50 points for predicting correctly.")
            else:
                add_score(user_id, -50)
                score_updates.append(f"User {user_id} lost 50 points for predicting incorrectly.")
            del user_votes[user_id]
    return score_updates

async def send_final_message(game_name, win, players_info, game_id):
    channel = client.get_channel(CHANNEL_ID)
    if channel:
        result = "won" if win else "lost"
        result_message = f"{game_name} has just finished a game and {result}!\n\n"

        score_updates = await update_scores(game_id, win)
        score_updates_message = "\n".join(score_updates) + "\n\n"

        users_info = get_users_info()
        sorted_users = sorted(users_info['users'], key=lambda x: x['score'], reverse=True)

        scores_message = "Current Scores:\n"
        for user in sorted_users:
            scores_message += f"User {user['discord_id']}: {user['score']}\n"

        await channel.send(result_message + score_updates_message + scores_message)

        # Clean up active_votes for this game
        active_vote_message_ids = [key for key, value in active_votes.items() if value == game_id]
        for message_id in active_vote_message_ids:
            del active_votes[message_id]

async def run_bot():
    if DISCORD_TOKEN:
        await client.start(DISCORD_TOKEN)
    else:
        print("Invalid bot token.")
