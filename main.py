from api import *
from logic import *
import time
# for all players in players.json add the last played game into checked_games.json
# from this game on new games will be considered valid to use for betting
log_last_game_bulk()

players_info = get_players_info()
if not players_info:
    print("No players found in players.json, quitting...")
    exit()
        
while True:
    # Iterate over each player in players.json
    for player_info in players_info:
        game_name = player_info["name"]
        tag_line = player_info["tag"]
        
        # Get the PUUID of the player
        puuid = get_account_puuid(game_name, tag_line)
        if "error" in puuid:
            print(f"Error fetching PUUID for {game_name}#{tag_line}: {puuid['error']}")
            continue
        # Check if active game
        active_game = get_active_game(puuid)
        if active_game == None:
            print(f"{game_name}#{tag_line} is not active!")
            continue
        
        print(f"{game_name}#{tag_line} is in a live game!")
                 
    time.sleep(20)  