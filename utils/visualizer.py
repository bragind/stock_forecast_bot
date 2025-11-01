# utils/visualizer.pyimport matplotlib
import matplotlib
matplotlib.use('Agg')  
import matplotlib.pyplot as plt
import os
from datetime import datetime, timedelta

def plot_forecast(history, forecast):
    plt.figure(figsize=(12, 6))
    plt.plot(history.index, history['Close'], label='История', color='blue')
    
    last_date = history.index[-1]
    forecast_dates = [last_date + timedelta(days=i) for i in range(1, 31)]
    plt.plot(forecast_dates, forecast, label='Прогноз', color='red', linestyle='--')
    
    plt.title('Прогноз цены акции на 30 дней')
    plt.xlabel('Дата')
    plt.ylabel('Цена, USD')
    plt.legend()
    plt.grid(True)
    
    img_path = f"forecast_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    plt.savefig(img_path)
    plt.close()
    return img_path
