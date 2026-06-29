"""
app.py
------
Streamlit dashboard for the Marvel Rivals Tier List Predictor.

Displays hero cards with images grouped by predicted tier (S/A/B/C/D).
Hero images are fetched from marvelrivalsapi.com using the imageUrl
field from raw_heros.csv.

Run with: streamlit run app.py
"""

import streamlit as st
import pandas as pd


def load_data():
    """Load hero tier predictions with image URLs."""
    data = pd.read_csv("hero_tiers.csv")
    return data


def render_tier(data, tier):
    """Render a row of hero cards for a given tier."""
    tier_heroes = data[data['tier'] == tier]
    if tier_heroes.empty:
        return

    st.subheader(f"{tier} Tier")
    cols = st.columns(len(tier_heroes))
    for i, (_, hero) in enumerate(tier_heroes.iterrows()):
        with cols[i]:
            img_url = f"https://marvelrivalsapi.com{hero['imageUrl']}"
            st.image(img_url, width=80)
            st.caption(hero['hero_name'])


if __name__ == "__main__" or True:
    st.title("Marvel Rivals Tier List Predictor")

    data = load_data()

    for tier in ['S', 'A', 'B', 'C', 'D']:
        render_tier(data, tier)