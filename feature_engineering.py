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

split['htm']=split['hours']*60


for splt in split:
    if splt['seconds']>=31:
        splt['seconds']=1
    else:
        splt['seconds']=0
split['stm']=split['seconds']
split['total_minutes']=split['htm']+split['minutes']+split['stm']
print(split.head())
