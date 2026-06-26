import pandas as pd
import numpy as np

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.preprocessing import LabelEncoder
from feature_engineering import features

data=pd.read_csv("raw_hero_stats.csv")
data=data.columns(features)
print(data)


