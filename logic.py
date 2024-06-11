from api import *
import json


     
def get_checked_games():
    """
    Retrieve the list of checked game IDs from the database.
    """
    try:
        with open("checked_games.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def add_checked_game(game_id):
    """
    Add a game ID to the database of checked games.
    """
    checked_games = get_checked_games()
    checked_games.append(game_id)
    with open("checked_games.json", "w") as file:
        json.dump(checked_games, file)
        
def log_last_game(puuid):
    """
    Log the last played game for a player into checked_games.json.
    
    Args:
    - puuid (str): The PUUID of the player.
    """
    match_ids = get_match_ids(puuid, count=1)
    if "error" in match_ids:
        print(f"Error fetching match IDs: {match_ids['error']}")
        return
    
    last_game_id = match_ids[0]
    checked_games = get_checked_games()
    if last_game_id not in checked_games:
        add_checked_game(last_game_id)
        print(f"Last played game {last_game_id} logged successfully.")
    else:
        print(f"Last played game {last_game_id} already logged.")

def log_last_game_bulk():
    """
    Log the last played game for all users specified in players.json.
    """
    # Load player information from players.json
    with open("players.json", "r") as file:
        players_info = json.load(file)["players"]
    
    # Iterate over each player and log the last played game
    for player_info in players_info:
        game_name = player_info["name"]
        tag_line = player_info["tag"]
        
        puuid = get_account_puuid(game_name, tag_line)
        if "error" in puuid:
            print(f"Error fetching PUUID for {game_name}#{tag_line}: {puuid['error']}")
            continue
        
        log_last_game(puuid)


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
