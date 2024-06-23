import os
import discord
import json
from logic import add_score, get_users_info, get_players_info
from discord.ext import commands

DISCORD_TOKEN = os.environ.get('DISCORD_TOKEN')
CHANNEL_ID = 1251180886284701767

intents = discord.Intents.default()
client = discord.Client(intents=intents)

active_votes = {}  # Dictionary to store active vote message IDs mapped to game IDs
user_votes = {}  

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
    if user.bot:
        return  # Ignore reactions from the bot itself

    if reaction.message.id in active_votes:
        game_id = active_votes[reaction.message.id]
        if str(reaction.emoji) == '💙':
            vote = "win"
        elif str(reaction.emoji) == '❤️':
            vote = "lose"
        else:
            return  # Ignore reactions other than 💙 and ❤️

        # Check if the user already has votes recorded
        if user.id in user_votes:
            user_votes[user.id].append({
                "game_id": game_id,
                "vote": vote,
                "vote_message_id": reaction.message.id
            })
        else:
            user_votes[user.id] = [{
                "game_id": game_id,
                "vote": vote,
                "vote_message_id": reaction.message.id
            }]

        print(f"{user.id} has voted {vote} for Game ID: {game_id}")


@client.event
async def on_reaction_remove(reaction, user):
    if reaction.message.id in active_votes:
        await reaction.message.add_reaction(reaction.emoji)

async def update_scores(game_id, win):
    score_updates = []
    bot_id = client.user.id  # Get the bot's user ID
    for user_id, votes_list in list(user_votes.items()):
        if user_id == bot_id:
            continue  # Skip the bot's own votes

        for votes in votes_list:
            if votes["game_id"] == game_id:
                # Fetch the member object to get display name
                member = await client.fetch_user(user_id)
                if member:
                    display_name = member.display_name
                    if (votes["vote"] == "win" and win) or (votes["vote"] == "lose" and not win):
                        add_score(user_id, 25)
                        score_updates.append(f"{display_name} gained 25 points for predicting correctly on Game ID: {game_id}.")
                    else:
                        add_score(user_id, -25)
                        score_updates.append(f"{display_name} lost 25 points for predicting incorrectly on Game ID: {game_id}.")
                
                # Remove this specific vote from the user's list of votes
                votes_list.remove(votes)

    return score_updates



async def send_final_message(game_name, win, game_id):
    channel = client.get_channel(CHANNEL_ID)
    if channel:
        result = "won" if win else "lost"
        result_message = f"{game_name} has just finished a game and {result}!\n\n"

        score_updates = await update_scores(game_id, win)
        score_updates_message = "\n".join(score_updates) + "\n\n"

        users_info = get_users_info()
        sorted_users = sorted(users_info['users'], key=lambda x: x['score'], reverse=True)

         # Create a formatted scoreboard message
        scores_message = "```\nScoreboard:\n"
        scores_message += f"{'Rank':<6} {'Username':<20} {'Score':<5}\n"
        scores_message += "-" * 34 + "\n"  # Add a separator line

        for rank, user in enumerate(sorted_users, start=1):
            member = await client.fetch_user(user['discord_id'])
            username = member.display_name
            scores_message += f"{rank:<6} {username:<20} {user['score']:<5}\n"

        scores_message += "```"  # Close the code block

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
