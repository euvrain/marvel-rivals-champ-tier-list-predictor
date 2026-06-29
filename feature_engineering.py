"""
features.py
-----------
Engineers features from raw hero stats for use in KMeans clustering.

Features engineered:
- winrate: wins / matches
- kda: kills / deaths (deaths floored at 1 to avoid division by zero)
- dmg_per_min, heal_per_min, dmg_taken_per_min: per-minute stats
- dmg_per_match, heal_per_match, dmg_taken_per_match: per-match stats
- hit_rate: session hit rate from API

play_time is parsed from "Xh Ym Zs" format. Seconds >= 31 are rounded
up to the next minute to approximate total minutes played.

Output: features.csv
"""

import pandas as pd


def parse_play_time(play_time_series):
    """Parse play_time string 'Xh Ym Zs' into total minutes."""
    split = play_time_series.str.extract(
        r'(?P<hours>\d+)h\s*(?P<minutes>\d+)m\s*(?P<seconds>\d+)s'
    ).astype(int)

    # round seconds >= 31 up to the next minute
    split['total_minutes'] = (
        split['hours'] * 60 +
        split['minutes'] +
        (split['seconds'] >= 31).astype(int)
    )
    return split['total_minutes']


def engineer_features(data):
    """Engineer all features from raw hero stats dataframe."""
    data['winrate'] = data['wins'] / data['matches']
    data['kda'] = data['k'] / data['d'].replace(0, 1)

    data['play_time_minutes'] = parse_play_time(data['play_time'])

    data['dmg_per_min'] = data['total_hero_damage'] / data['play_time_minutes']
    data['heal_per_min'] = data['total_hero_heal'] / data['play_time_minutes']
    data['dmg_taken_per_min'] = data['total_damage_taken'] / data['play_time_minutes']

    data['dmg_per_match'] = data['total_hero_damage'] / data['matches']
    data['heal_per_match'] = data['total_hero_heal'] / data['matches']
    data['dmg_taken_per_match'] = data['total_damage_taken'] / data['matches']

    data['hit_rate'] = data['session_hit_rate']

    return data


if __name__ == "__main__":
    data = pd.read_csv("raw_hero_stats.csv")
    data = engineer_features(data)

    feature_cols = [
        'hero_name', 'winrate', 'kda',
        'dmg_per_min', 'heal_per_min', 'dmg_taken_per_min',
        'dmg_per_match', 'heal_per_match', 'dmg_taken_per_match',
        'hit_rate'
    ]

    data[feature_cols].to_csv("features.csv", index=False)
    print(f"saved {len(data)} heroes to features.csv")