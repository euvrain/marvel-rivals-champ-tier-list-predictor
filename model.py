"""
model.py
--------
Clusters Marvel Rivals heroes into S/A/B/C/D tiers using KMeans.

Approach:
- Merges role metadata to enable role-normalized feature engineering
- Normalizes dmg, heal, and dmg_taken within each role so heroes are
  compared against others in their role, not across all roles
- Scales features with StandardScaler before clustering
- Maps clusters to tiers based on average winrate per cluster

Limitation: stat-based clustering underrates utility-heavy heroes
(e.g. Rocket Raccoon, Storm) whose value comes from ability kit
impact not captured in raw stats.

Output: hero_tiers.csv
"""

import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


def normalize_by_role(data):
    """Normalize key stats within each role to enable fair cross-hero comparison."""
    for col, new_col in [
        ('dmg_per_min', 'dps_norm'),
        ('heal_per_min', 'sup_norm'),
        ('dmg_taken_per_min', 'tank_norm')
    ]:
        data[new_col] = data.groupby('role')[col].transform(
            lambda x: (x - x.mean()) / x.std()
        )
    return data


def cluster_heroes(data, feature_cols, n_clusters=5):
    """Scale features and fit KMeans clustering."""
    X = data[feature_cols]
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    model = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    data['cluster'] = model.fit_predict(X_scaled)
    return data


def assign_tiers(data):
    """Map clusters to S/A/B/C/D based on average winrate per cluster."""
    cluster_winrates = data.groupby('cluster')['winrate'].mean().sort_values(ascending=False)
    tier_labels = ['S', 'A', 'B', 'C', 'D']
    tier_map = {cluster: tier for cluster, tier in zip(cluster_winrates.index, tier_labels)}
    data['tier'] = data['cluster'].map(tier_map)
    return data


if __name__ == "__main__":
    data = pd.read_csv("features.csv")
    heroes_meta = pd.read_csv("raw_heros.csv")[['name', 'role', 'imageUrl']]
    data = data.merge(heroes_meta, left_on='hero_name', right_on='name').drop(columns=['name'])

    data = normalize_by_role(data)

    feature_cols = ['winrate', 'kda', 'dps_norm', 'sup_norm', 'tank_norm', 'hit_rate']
    data = cluster_heroes(data, feature_cols)
    data = assign_tiers(data)

    print(data[['hero_name', 'tier', 'winrate']].sort_values('tier'))
    data.to_csv("hero_tiers.csv", index=False)
    print(f"\nsaved {len(data)} heroes to hero_tiers.csv")