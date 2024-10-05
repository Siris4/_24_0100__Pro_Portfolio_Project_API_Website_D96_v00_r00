import requests

# Your Riot API Key
API_KEY = 'YOUR_RIOT_API_KEY'

# Base URL for the Riot API
BASE_URL = 'https://REGION.api.riotgames.com'


# Function to get Summoner ID from Summoner Name
def get_summoner_id(summoner_name, region='na1'):
    url = f'{BASE_URL}/lol/summoner/v4/summoners/by-name/{summoner_name}'
    headers = {'X-Riot-Token': API_KEY}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()['id']
    else:
        print(f"Error fetching summoner ID: {response.status_code}")
        return None


# Function to get live game data using Summoner ID
def get_live_game(summoner_id, region='na1'):
    url = f'{BASE_URL}/lol/spectator/v4/active-games/by-summoner/{summoner_id}'
    headers = {'X-Riot-Token': API_KEY}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    elif response.status_code == 404:
        print("Summoner is not currently in a live game.")
        return None
    else:
        print(f"Error fetching live game data: {response.status_code}")
        return None


# Function to extract and display live game details
def extract_game_details(game_data):
    participants = game_data['participants']
    game_queue_id = game_data['gameQueueConfigId']

    print(f"Game Queue ID: {game_queue_id}")
    if game_queue_id == 450:
        print("This is an ARAM match.")
    else:
        print(f"Other game mode detected, Queue ID: {game_queue_id}")

    for participant in participants:
        summoner_name = participant['summonerName']
        champion_id = participant['championId']
        summoner_spells = (participant['spell1Id'], participant['spell2Id'])
        runes = participant['perks']['perkIds']

        print(f"Summoner: {summoner_name}")
        print(f"Champion ID: {champion_id}")
        print(f"Summoner Spells: {summoner_spells}")
        print(f"Runes: {runes}")
        print("-------------------------")


# Main function to monitor live game
def live_game_monitor(summoner_name, region='na1'):
    # Get Summoner ID
    summoner_id = get_summoner_id(summoner_name, region)
    if summoner_id is None:
        print("Could not find summoner.")
        return

    # Get Live Game Data
    game_data = get_live_game(summoner_id, region)
    if game_data is None:
        print("Summoner is not in a live game.")
        return

    # Extract and Display Game Details
    extract_game_details(game_data)


# Example usage
summoner_name = "YourSummonerName"  # Replace with your actual Summoner Name
live_game_monitor(summoner_name)
