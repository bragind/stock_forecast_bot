# models/nn_model.py
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_absolute_percentage_error, mean_squared_error
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

def train_lstm_model(df):
    data = df['Close'].values.reshape(-1, 1)
    scaler = MinMaxScaler()
    scaled_data = scaler.fit_transform(data)

    def create_sequences(data, seq_len=60):
        X, y = [], []
        for i in range(seq_len, len(data)):
            X.append(data[i-seq_len:i, 0])
            y.append(data[i, 0])
        return np.array(X), np.array(y)

    seq_len = 60
    X, y = create_sequences(scaled_data, seq_len)
    split = int(len(X) * 0.8)
    X_train, X_test = X[:split], X[split:]
    y_train, y_test = y[:split], y[split:]

    X_train = X_train.reshape((X_train.shape[0], X_train.shape[1], 1))
    X_test = X_test.reshape((X_test.shape[0], X_test.shape[1], 1))

    model = Sequential([
        LSTM(50, return_sequences=True, input_shape=(seq_len, 1)),
        LSTM(50),
        Dense(1)
    ])
    model.compile(optimizer='adam', loss='mse')
    model.fit(X_train, y_train, epochs=10, batch_size=32, verbose=0)

    y_pred_scaled = model.predict(X_test, verbose=0)
    y_pred = scaler.inverse_transform(y_pred_scaled).flatten()
    y_true = scaler.inverse_transform(y_test.reshape(-1, 1)).flatten()

    mape = mean_absolute_percentage_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))

    # Прогноз на 30 дней
    last_seq = scaled_data[-seq_len:].reshape(1, seq_len, 1)
    forecast_scaled = []
    for _ in range(30):
        pred = model.predict(last_seq, verbose=0)[0, 0]
        forecast_scaled.append(pred)
        last_seq = np.append(last_seq[:, 1:, :], [[[pred]]], axis=1)

    forecast = scaler.inverse_transform(np.array(forecast_scaled).reshape(-1, 1)).flatten()

    return {
        "forecast": forecast.tolist(),
        "mape": mape,
        "rmse": rmse
    }