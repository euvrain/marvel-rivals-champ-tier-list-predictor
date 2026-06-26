import pandas as pd


data=pd.read_csv("raw_hero_stats.csv")

print(data.head())

winrate=data['wins']/data['matches']
print(winrate.head())
for i in range(len(data['d'])):
    if data['d'][i]==0:
        kda = data['k']/((data['d'] + 1))
    else:
        kda = data['k']/data['d']
print(kda.head())

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


#healing per min
data['heal_per_min']=data['total_hero_heal']/data['play_time_minutes']
print(data['heal_per_min'].head())