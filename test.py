import logic as l
import api as a
import asyncio



name = "B0LULU"
tag = "EUW"

puuid = l.get_account_puuid(name, tag)
print(puuid)
game = l.get_active_game(puuid)

print(len(game))


