# models/model_selector.py
from .ml_model import train_rf_model
from .stats_model import train_prophet_model
from .nn_model import train_lstm_model

def select_best_model(df):
    models = {
        "Random Forest": train_rf_model(df),
        "Prophet": train_prophet_model(df),
        #"LSTM": train_lstm_model(df)
    }

    # Выбираем по MAPE
    best_name = min(models, key=lambda k: models[k]["mape"])
    best = models[best_name]

    return {
        "forecast": best["forecast"],
        "model_name": best_name,
        "metric": "MAPE",
        "metric_value": best["mape"]
    }
