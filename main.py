from api import *
from logic import *
import time
import json

# Global list to track ongoing games
ongoing_games = []


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
        

        for puuid, game_id in ongoing_games[:]:
            active_game = get_active_game(puuid)
            if active_game is None:
                # Game has ended
                player_info = next((p for p in players_info if get_account_puuid(p["name"], p["tag"]) == puuid), None)
                if player_info:
                    game_name = player_info["name"]
                    tag_line = player_info["tag"]
                    win = is_game_win(puuid, game_id)
                ongoing_games.remove((puuid, game_id))
                if win:
                    print(f"{game_name}#{tag_line} has just finished a game and won!")                 
                else:
                    print(f"{game_name}#{tag_line} has just finished a game and lost!")
            else:
                print(f"{game_name}#{tag_line} is currently in a game!")
        
        
        active_game = get_active_game(puuid)
        if not active_game:
            print(f"{game_name}#{tag_line} is not active!")
            continue
        
        # Check if active game is a new game
        game_id = "EUW1_" + str(active_game.get("gameId"))
        if game_id and (puuid,game_id) not in ongoing_games:
            print(f"{game_name}#{tag_line} is in a new live game! (Game ID: {game_id})")
            ongoing_games.append((puuid, game_id))         
    time.sleep(30)  