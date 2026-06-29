import pandas as pd


data=pd.read_csv("raw_hero_stats.csv")

print(data.head())
feature_cols=[]
#kda and winrate
data['winrate']=data['wins']/data['matches']


print(data['winrate'].head())

data['kda']=data['k']/(data['d']).replace(0,1)
print(data['kda'].head())
feature_cols.append('kda')
feature_cols.append('winrate')
#damage per min

split=data['play_time'].str.extract(r'(?P<hours>\d+)h\s*(?P<minutes>\d+)m\s*(?P<seconds>\d+)s')
split.columns = ['hours', 'minutes', 'seconds']
print(split)
split['hours']=split['hours'].astype(int)
split['minutes']=split['minutes'].astype(int)
split['seconds']=split['seconds'].astype(int)

split['htm']=split['hours']*60
print(split.head())
split['seconds'] = (split['seconds'].astype(int) >= 31).astype(int)
split['stm']=split['seconds']
split['total_minutes']=split['htm']+split['minutes']+split['stm']
print(split.head())

data["play_time_minutes"]=split['total_minutes']
data['dmg_per_min'] = data['total_hero_damage']/data['play_time_minutes']
print(data['dmg_per_min'].head())
feature_cols.append('dmg_per_min')

#healing per min
data['heal_per_min']=data['total_hero_heal']/data['play_time_minutes']
print(data['heal_per_min'].head())
feature_cols.append('heal_per_min')
#damage taken per min
data['dmg_taken_per_min']=data['total_damage_taken']/data['play_time_minutes']
print(data['dmg_taken_per_min'].head())
feature_cols.append('dmg_taken_per_min')

#damage per match
data['dmg_per_match']=data['total_hero_damage']/data['matches']
feature_cols.append('dmg_per_match')
#healing per match 
data['heal_per_match']=data['total_hero_heal']/data['matches']
feature_cols.append('heal_per_match')
#damage taken per match
data['dmg_taken_per_match']=data['total_damage_taken']/data['matches']
feature_cols.append('dmg_taken_per_match')
#hitrate
data['hit_rate']=data['session_hit_rate']

feature_cols.append('hit_rate')

X=data[feature_cols]
X.to_csv("features.csv", index=False)