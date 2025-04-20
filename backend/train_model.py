
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import joblib

df = pd.read_csv("data/words_dataset.csv")
df['hints_used'] = [1] * len(df)
df['time_taken'] = [5.0] * len(df)
df['difficulty_score'] = df['word_length'] * 0.5 + df['hints_used'] * 2 + df['time_taken'] * 0.1 + (1 - df['word_frequency']) * 5

X = df[['hints_used', 'time_taken', 'word_length', 'word_frequency']]
y = df['difficulty_score']

model = RandomForestRegressor()
model.fit(X, y)

joblib.dump(model, 'models/difficulty_model.pkl')
