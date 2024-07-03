import logic as l
import api as a
import asyncio



name = "wewo"
tag = "jung"

puuid = l.get_account_puuid(name, tag)

print(puuid)



