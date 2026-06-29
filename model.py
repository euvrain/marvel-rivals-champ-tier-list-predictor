import pandas as pd
import numpy as np

from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import classification_report
from sklearn.preprocessing import LabelEncoder
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
data=pd.read_csv("features.csv")
print(data.shape)
print(data.head())


heroes_meta = pd.read_csv("raw_heros.csv")[['name', 'role']]
data = data.merge(heroes_meta, left_on='hero_name', right_on='name').drop(columns=['name'])


dps_hero=data[data['role']=='Duelist'].drop(columns=['hero_name'])
sup_hero = data[data['role']=='Strategist'].drop(columns=['hero_name'])
tank_hero = data[data['role']=='Vanguard'].drop(columns=['hero_name'])


data['dps_norm'] = data.groupby('role')['dmg_per_min'].transform(
    lambda x: (x - x.mean()) / x.std()
)
data['sup_norm'] = data.groupby('role')['heal_per_min'].transform(
    lambda x: (x - x.mean()) / x.std()
)
data['tank_norm'] = data.groupby('role')['dmg_taken_per_min'].transform(
    lambda x: (x - x.mean()) / x.std()
)

# defining X
feature_cols=data.drop(columns=['hero_name']).columns.select_dtypes(include='float64')
X=data[feature_cols]

#preprocessing
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)  




print(feature_cols.head)

#model
model = KMeans(n_clusters=5, random_state=42)

model.fit(X_scaled)
data['cluster'] = model.predict(X_scaled)

for cluster in sorted(data['cluster'].unique()):
    heroes = data[data['cluster'] == cluster]['hero_name'].tolist()
    print(f"cluster {cluster}: {heroes}")

cluster_stats = data.groupby('cluster')['winrate'].mean().sort_values(ascending=False)
print(cluster_stats)
tier_map = {
    2: 'DPS', 
    0: 'Strategist',
    3: 'D',
    1: 'Tank',
    4: 'DPS' 
}

data['tier'] = data['cluster'].map(tier_map)
print(data[['hero_name', 'tier']].sort_values('tier'))

