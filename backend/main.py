
from fastapi import FastAPI, Request
from pydantic import BaseModel
import random
import pandas as pd
import joblib

app = FastAPI()

words_df = pd.read_csv("data/words_dataset.csv")
model = joblib.load("models/difficulty_model.pkl")

class GameData(BaseModel):
    hints_used: int
    time_taken: float
    word_length: int
    word_frequency: float

@app.get("/start_game")
def start_game():
    word_row = words_df.sample(1).iloc[0]
    return {
        "word": "_" * word_row['word_length'],
        "length": word_row['word_length'],
        "frequency": word_row['word_frequency'],
        "true_word": word_row['word']  # For testing only
    }

@app.post("/predict_difficulty")
def predict_difficulty(data: GameData):
    features = [[data.hints_used, data.time_taken, data.word_length, data.word_frequency]]
    difficulty = model.predict(features)[0]
    return {"predicted_difficulty": round(difficulty, 2)}
