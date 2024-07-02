import logic as l
import api as a
import asyncio



name = "bcnbv"
tag = "Aegis"
puuid = a.get_account_puuid(name, tag)
print(puuid)

game = a.get_active_game(puuid)
print(game)

champion_list = l.get_champion_list()

if game:
    result  = asyncio.run(l.get_champion_name(game, puuid, champion_list))
    print(result)



