import logic as l
import api as a


name = "Bal"
tag = "Chant"
puuid = a.get_account_puuid(name, tag)
print(puuid)

