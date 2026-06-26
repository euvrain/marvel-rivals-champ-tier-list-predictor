import requests
import pandas as pd

API_KEY = "6e1deb4a15d7732b610ace74b06e73af2f3632d1e06799c4d11b39ed38e60864"
BASE_URL = "https://marvelrivalsapi.com/api/v1"
HEADERS = {"x-api-key": API_KEY}

# First get all hero names
heroes_resp = requests.get(f"{BASE_URL}/heroes", headers=HEADERS)
heroes = heroes_resp.json()  # list of hero objects
heroes=pd.DataFrame(heroes)
print(heroes.columns)
hero_names=heroes['name']
# print(names)

# hero_names=heroes['name']
heroes.to_csv("raw_heros.csv", index=False)

# Second get stat and match data
hero_stats = requests.get(f"{BASE_URL}/heroes/hero/:hero/stats", headers=HEADERS).json()
# Then loop and collect stats for each
# records = []
# for hero in heroes:
#     name = hero["name"]
#     stats_resp = requests.get(f"{BASE_URL}/heroes/hero/{name}/stats", headers=HEADERS)
#     if stats_resp.status_code == 200:
#         records.append(stats_resp.json())

# df = pd.DataFrame(records)
# df.to_csv("raw_hero_stats.csv", index=False)
