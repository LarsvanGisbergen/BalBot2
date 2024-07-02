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

def get_champion_list_with_icons():
    """
    Fetches the list of champions with their IDs, names, and icons from Data Dragon.

    Returns:
    dict: Dictionary mapping champion IDs to their names and icons.
    """
    # Define the Data Dragon version (can be dynamically fetched from Riot if needed)
    version = '6.24.1'
    # Define the endpoint URL for the champion list from Data Dragon
    url = f"http://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/champion.json"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad response status
        
        champions_data = response.json()['data']
        
        # Create a dictionary with champion ID, name, and icon URL
        champion_list = {}
        for champion_key, champion_info in champions_data.items():
            champion_id = int(champion_info['key'])
            champion_name = champion_info['name']
            # Construct the icon URL using champion ID
            icon_url = f"https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/champion-icons/{champion_id}.png"
            champion_list[champion_id] = {
                'name': champion_name,
                'icon_url': icon_url
            }
        
        return champion_list
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching champion data: {e}")
    
    return None
