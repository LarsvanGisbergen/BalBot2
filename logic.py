from api import *
import json


def get_players_info():
    """
    Retrieve player names and tags for all players in players.json.

    Returns:
    - list: A list containing dictionaries with player names and tags.
    """
    try:
        with open("players.json", "r") as file:
            players_data = json.load(file)
            return players_data["players"]
    except FileNotFoundError:
        print("players.json file not found.")
        return None

def get_match_details(game_id):
    """
    Retrieve detailed match information for a given game ID.

    Args:
    - game_id (str): The ID of the game.

    Returns:
    - dict: Dictionary containing match details.
    """
    api_key = get_riot_api_key()
    url = f"https://europe.api.riotgames.com/lol/match/v5/matches/{game_id}"
    headers = {"X-Riot-Token": api_key}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching match details: {response.status_code} - {response.text}")
        return {}
    

def is_game_win(puuid, game_id):
    """
    Determine if the last game was a win or loss for the player.

    Args:
    - game_name (str): The game name of the player.
    - tag_line (str): The tag line of the player.
    - puuid (str): The PUUID of the player.
    - game_id (str): The ID of the game.

    Returns:
    - bool: True if the game was a win, False otherwise.
    """
    match_details = get_match_details(game_id)
    if not match_details:
        print(f"Could not fetch match details for game ID {game_id}")
        return False

    # Iterate through participant list to find the player's results
    for participant in match_details.get("info", {}).get("participants", []):
        if participant["puuid"] == puuid:
            return participant["win"]

    print(f"Player with PUUID {puuid} not found in game ID {game_id}")
    return False
    
def get_users_info():
    with open('users.json', 'r') as f:
        return json.load(f)

def add_score(discord_id, score):
    with open('users.json', 'r') as f:
        users_info = json.load(f)

    for user in users_info['users']:
        if user['discord_id'] == discord_id:
            user['score'] += score
            break

    with open('users.json', 'w') as f:
        json.dump(users_info, f, indent=4)
    
