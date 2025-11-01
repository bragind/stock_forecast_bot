# utils/data_loader.py
import yfinance as yf
import pandas as pd

def load_stock_data(ticker: str, period="2y") -> pd.DataFrame:
    data = yf.download(ticker, period=period, auto_adjust=True)
    
    if data.empty:
        raise ValueError("Данные не найдены. Проверьте правильность тикера.")

    # Обработка мультииндекса
    if isinstance(data.columns, pd.MultiIndex):
        # Оставляем только уровень 0 (например, 'Close')
        data.columns = data.columns.get_level_values(0)

    # Убедимся, что есть 'Close'
    if 'Close' not in data.columns:
        raise ValueError(f"Колонка 'Close' отсутствует. Доступные колонки: {list(data.columns)}")

    data = data[['Close']].dropna()

    if data.empty:
        raise ValueError("После очистки данных не осталось записей.")

    return data