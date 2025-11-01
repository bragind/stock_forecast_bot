# models/stats_model.py
import pandas as pd
from prophet import Prophet
from sklearn.metrics import mean_absolute_percentage_error, mean_squared_error
import numpy as np

def train_prophet_model(df):
    df = df.reset_index()
    df.columns = ['ds', 'y']
    split = int(len(df) * 0.8)
    train, test = df[:split], df[split:]

    model = Prophet(daily_seasonality=False, yearly_seasonality=True)
    model.fit(train)

    future = model.make_future_dataframe(periods=len(test) + 30)
    forecast_full = model.predict(future)
    y_pred_test = forecast_full.iloc[split:split+len(test)]['yhat'].values
    y_true_test = test['y'].values

    mape = mean_absolute_percentage_error(y_true_test, y_pred_test)
    rmse = np.sqrt(mean_squared_error(y_true_test, y_pred_test))

    forecast_30 = forecast_full.iloc[-30:]['yhat'].values

    return {
        "forecast": forecast_30.tolist(),
        "mape": mape,
        "rmse": rmse
    }