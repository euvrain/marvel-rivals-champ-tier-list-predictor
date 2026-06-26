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

