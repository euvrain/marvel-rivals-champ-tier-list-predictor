"""
collect.py
----------
Fetches hero metadata and per-hero stats from the Marvel Rivals API.
Saves raw data to raw_heros.csv and raw_hero_stats.csv for downstream
feature engineering and modeling.

API: https://marvelrivalsapi.com
Rate limit: 3,000 requests/day (free tier), ~1 req/2s to avoid 429s
"""

import requests
import pandas as pd
import time
import urllib.parse
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
BASE_URL = "https://marvelrivalsapi.com/api/v1"
HEADERS = {"x-api-key": API_KEY}


def fetch_heroes():
    """Fetch all heroes and save metadata to raw_heros.csv."""
    resp = requests.get(f"{BASE_URL}/heroes", headers=HEADERS)
    heroes = pd.DataFrame(resp.json())
    heroes['name'] = heroes['name'].str.lower()  # normalize for API queries
    heroes.to_csv("raw_heros.csv", index=False)
    return heroes['name']


def fetch_hero_stats(hero_names):
    """
    Fetch per-hero stats for each hero in hero_names.
    Handles 429 rate limiting with a 120s backoff and single retry.
    Names are URL-encoded to handle special characters (e.g. cloak & dagger).
    """
    records = []
    for name in hero_names:
        encoded = urllib.parse.quote(name)
        resp = requests.get(f"{BASE_URL}/heroes/hero/{encoded}/stats", headers=HEADERS)

        if resp.status_code == 200:
            records.append(resp.json())
            print(f"✓ {name}")
        elif resp.status_code == 429:
            # free tier rate limit hit — wait and retry once
            print(f" rate limited on {name}, waiting 120s...")
            time.sleep(120)
            retry = requests.get(f"{BASE_URL}/heroes/hero/{encoded}/stats", headers=HEADERS)
            if retry.status_code == 200:
                records.append(retry.json())
                print(f"✓ {name} (retry)")
            else:
                print(f"✗ {name} failed after retry — {retry.status_code}")
        elif resp.status_code == 400:
            print(f"✗ {name} — bad name format")
        elif resp.status_code == 404:
            print(f"✗ {name} — no stats available yet")
        elif resp.status_code == 401:
            print("✗ API key invalid, stopping")
            break

        time.sleep(2)  # stay under rate limit between requests
    return records


if __name__ == "__main__":
    hero_names = fetch_heroes()
    records = fetch_hero_stats(hero_names)
    pd.DataFrame(records).to_csv("raw_hero_stats.csv", index=False)
    print(f"\ncollected {len(records)}/{len(hero_names)} heroes")