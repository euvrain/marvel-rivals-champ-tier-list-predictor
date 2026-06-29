import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

data = pd.read_csv("features.csv")
heroes_meta = pd.read_csv("raw_heros.csv")[['name', 'role']]
data = data.merge(heroes_meta, left_on='hero_name', right_on='name').drop(columns=['name'])

data['dps_norm'] = data.groupby('role')['dmg_per_min'].transform(
    lambda x: (x - x.mean()) / x.std()
)
data['sup_norm'] = data.groupby('role')['heal_per_min'].transform(
    lambda x: (x - x.mean()) / x.std()
)
data['tank_norm'] = data.groupby('role')['dmg_taken_per_min'].transform(
    lambda x: (x - x.mean()) / x.std()
)

feature_cols = ['winrate', 'kda', 'dps_norm', 'sup_norm', 'tank_norm', 'hit_rate']
X = data[feature_cols]

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

model = KMeans(n_clusters=5, random_state=42, n_init=10)
data['cluster'] = model.fit_predict(X_scaled)

for cluster in sorted(data['cluster'].unique()):
    heroes = data[data['cluster'] == cluster]['hero_name'].tolist()
    print(f"cluster {cluster}: {heroes}")

cluster_stats = data.groupby('cluster')['winrate'].mean().sort_values(ascending=False)
print("\nwinrate by cluster:")
print(cluster_stats)

tier = {2: 'B', 4: 'C', 0: 'S', 3: 'A', 1: 'D'}
data['tier'] = data['cluster'].map(tier) 
print(f"\nhero tiers: {data[['hero_name','tier']]}")