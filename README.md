# Marvel Rivals Tier List Predictor

An unsupervised ML pipeline that predicts hero tiers in Marvel Rivals 
using real game stats from the Marvel Rivals API.

## How it works

1. **Data Collection** — fetches hero stats for all 40 heroes from the 
   Marvel Rivals API with rate limit handling
2. **Feature Engineering** — engineers role-normalized features including 
   win rate, KDA, damage/healing/damage-taken per minute and per match
3. **Modeling** — KMeans clustering (k=5) on role-normalized features 
   to group heroes into S/A/B/C/D tiers
4. **Dashboard** — Streamlit app displaying hero cards with images 
   grouped by predicted tier

## Tech stack
- Python, pandas, scikit-learn, Streamlit
- Marvel Rivals API (marvelrivalsapi.com)

## Key insight
Pure stat-based clustering captures role archetypes well but 
underrates utility-heavy heroes like Rocket Raccoon and Storm, 
whose value comes from ability kit impact rather than raw stats. 
This is a known limitation of stat-only ML approaches for hero 
tier prediction.

## Run locally
```bash
pip install -r requirements.txt
python collect.py       # fetch hero stats
python features.py      # engineer features  
python model.py         # cluster into tiers
streamlit run app.py    # launch dashboard
```

## Project structure
```
├── collect.py      # API data collection
├── features.py     # feature engineering
├── model.py        # KMeans clustering
├── app.py          # Streamlit dashboard
├── data/           # raw and processed CSVs
└── models/         # saved model artifacts
```
