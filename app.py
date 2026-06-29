import streamlit as st
import pandas as pd

st.title("Hero Clustering and Tier Assignment")

hero_tiers=pd.read_csv("hero_tiers.csv")

