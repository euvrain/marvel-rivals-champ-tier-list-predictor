import streamlit as st
import pandas as pd

st.title("Marvel Rivals Tier List Predictor")

data=pd.read_csv("hero_tiers.csv")

data['imageUrl']= pd.read_csv("raw_heros.csv")[['imageUrl']]

# group by tier and display
for tier in ['S', 'A', 'B', 'C', 'D']:
    st.subheader(f"{tier} Tier")
    tier_heroes = data[data['tier'] == tier]
    
    cols = st.columns(len(tier_heroes))
    for i, (_, hero) in enumerate(tier_heroes.iterrows()):
        with cols[i]:
            img_url = f"https://marvelrivalsapi.com{hero['imageUrl']}"
            st.image(img_url, width=80)
            st.caption(hero['hero_name'])