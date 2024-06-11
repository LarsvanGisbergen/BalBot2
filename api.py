import os
import requests

def get_riot_api_key():
    """
    Retrieve Riot API key from environment variable.
    """
    api_key = os.environ.get('RIOT_API_KEY')
    if api_key is None:
        raise ValueError("Riot API key is not set. Please set the RIOT_API_KEY environment variable.")
    return api_key

def get_account_puuid(game_name, tag_line):
    """
    Retrieve the PUUID of a player based on game name and tag line.
    """
    api_key = get_riot_api_key()
    url = f"https://europe.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}"
    headers = {"X-Riot-Token": api_key}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()["puuid"]
    else:
        return {"error": response.status_code, "message": response.text}



def get_match_ids(puuid, count=1):
    """
    Retrieve match history for a player based on their PUUID.

    Args:
    - puuid (str): The PUUID of the player.
    - count (int): The number of match IDs to fetch. Default is 1.

    Returns:
    - list: A list of match IDs.
    """
    api_key = get_riot_api_key()
    url = f"https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids"
    headers = {"X-Riot-Token": api_key}
    params = {"count": count}
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": response.status_code, "message": response.text}


def get_active_game(encrypted_puuid):
    """
    Retrieve active game information for a summoner.

    Args:
    - encrypted_puuid (str): The encrypted PUUID of the summoner.

    Returns:
    - dict: Dictionary containing active game information if available, otherwise an empty dictionary.
            If the player is not currently in game, returns None.
    """
    api_key = get_riot_api_key()
    url = f"https://euw1.api.riotgames.com/lol/spectator/v5/active-games/by-summoner/{encrypted_puuid}"
    headers = {"X-Riot-Token": api_key}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 404:
        # Player is not in game
        return None
    else:
        print(f"Error fetching active game information: {response.status_code} - {response.text}")
        return None
