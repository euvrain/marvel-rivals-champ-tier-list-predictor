import requests
import pandas as pd
import time
from dotenv import load_dotenv
import os
import urllib.parse

load_dotenv()
API_KEY = os.getenv("API_KEY")
BASE_URL = "https://marvelrivalsapi.com/api/v1"
HEADERS = {"x-api-key": API_KEY}

# First get all hero names

heroes_resp = requests.get(f"{BASE_URL}/heroes", headers=HEADERS)
heroes = heroes_resp.json()  # list of hero objects
heroes=pd.DataFrame(heroes)
heroes['name'] = heroes['name'].str.lower()
print(heroes.columns)
hero_names=heroes['name']


# hero_names=heroes['name']
heroes.to_csv("raw_heros.csv", index=False)

# Second get stat and match data
records = []
for name in hero_names:
    name = urllib.parse.quote(name) 
    stats_resp = requests.get(f"{BASE_URL}/heroes/hero/{name}/stats", headers=HEADERS)
    
    if stats_resp.status_code == 200:
        records.append(stats_resp.json())
        print(f"✓ {name}")
    elif stats_resp.status_code == 429:
        print(f" rate limited on {name}, waiting 60s...")
        time.sleep(60)
        retry = requests.get(f"{BASE_URL}/heroes/hero/{name}/stats", headers=HEADERS)
        if retry.status_code == 200:
            records.append(retry.json())
            print(f"✓ {name} (retry)")
        else:
            print(f"✗ {name} failed after retry — {retry.status_code}")
    elif stats_resp.status_code == 400:
        print(f"✗ {name} — bad name format")
    elif stats_resp.status_code == 404:
        print(f"✗ {name} — no stats available yet")
    elif stats_resp.status_code == 401:
        print("✗ API key invalid, stopping")
        break
    
    time.sleep(2)

df = pd.DataFrame(records)
df.to_csv("raw_hero_stats.csv", index=False)