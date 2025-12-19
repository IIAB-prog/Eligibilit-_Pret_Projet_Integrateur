# api.py
import joblib
import pandas as pd

model = joblib.load("eligibilite_pret_model.pkl")

def predict_loan(data: dict):
    df = pd.DataFrame([data])
    prediction = model.predict(df)[0]
    return prediction
