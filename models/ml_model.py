# models/ml_model.py
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_percentage_error, mean_squared_error
import numpy as np

def create_lags(series, n_lags=5):
    df = pd.DataFrame(series)
    for lag in range(1, n_lags + 1):
        df[f'lag_{lag}'] = df['Close'].shift(lag)
    return df.dropna()

def train_rf_model(df):
    df_lagged = create_lags(df['Close'])
    X = df_lagged.drop(columns=['Close'])
    y = df_lagged['Close']
    split = int(len(X) * 0.8)
    X_train, X_test = X[:split], X[split:]
    y_train, y_test = y[:split], y[split:]

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    mape = mean_absolute_percentage_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))

    # Прогноз на 30 дней вперёд (рекурсивно)
    last_window = X.iloc[-1:].values
    forecast = []
    for _ in range(30):
        pred = model.predict(last_window)[0]
        forecast.append(pred)
        # Обновляем окно
        new_row = np.roll(last_window[0], -1)
        new_row[-1] = pred
        last_window = new_row.reshape(1, -1)

    return {
        "forecast": forecast,
        "mape": mape,
        "rmse": rmse
    }