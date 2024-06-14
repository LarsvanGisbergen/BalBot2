from api import *
from logic import *
import time
import json
from bot import *
import asyncio


async def run_main(refresh_rate):
    players_info = get_players_info()
    if not players_info:
        print("No players found in players.json, quitting...")
        return
    
    ongoing_games = []

    while True:
        for player_info in players_info:
            game_name = player_info["name"]
            tag_line = player_info["tag"]
            
            puuid = get_account_puuid(game_name, tag_line)
            if "error" in puuid:
                print(f"Error fetching PUUID for {game_name}#{tag_line}: {puuid['error']}")
                continue

            active_game = get_active_game(puuid)
            if active_game:
                game_id = "EUW1_" + str(active_game.get("gameId"))
                if (puuid, game_id) not in ongoing_games:
                    print(f"{game_name}#{tag_line} is in a new live game! (Game ID: {game_id})")
                    ongoing_games.append((puuid, game_id))
                    await send_vote_message(game_id, f"{game_name}#{tag_line}")
                else:
                    print(f"{game_name}#{tag_line} is currently in a game! (Game ID: {game_id})")
            else:
                print(f"{game_name}#{tag_line} is not active!")
                for puuid, game_id in ongoing_games[:]:
                    active_game_check = get_active_game(puuid)
                    if active_game_check is None:
                        player_info = next((p for p in players_info if get_account_puuid(p["name"], p["tag"]) == puuid), None)
                        if player_info:
                            game_name = player_info["name"]
                            tag_line = player_info["tag"]
                            win = is_game_win(puuid, game_id)
                          
                        if win:
                            print(f"{game_name}#{tag_line} has just finished a game and won!")
                        else:
                            print(f"{game_name}#{tag_line} has just finished a game and lost!")

                        await send_final_message(game_name, win, players_info, game_id)
                        ongoing_games.remove((puuid, game_id))

        await asyncio.sleep(refresh_rate)


async def main_loop(refresh_rate):
    while True:
        await run_main(refresh_rate)
        await asyncio.sleep(refresh_rate)

async def main():
    refresh_rate = 30  # seconds

    bot_task = asyncio.create_task(run_bot())
    await asyncio.sleep(10)  # Wait 10 seconds after starting run_bot

    loop_task = asyncio.create_task(main_loop(refresh_rate))
    await asyncio.gather(bot_task, loop_task)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except RuntimeError:
        pass  # Prevent RuntimeError due to re-running asyncio.run()