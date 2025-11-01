# utils/visualizer.py
import matplotlib
matplotlib.use('Agg')  
import matplotlib.pyplot as plt
import pandas as pd
import os
from datetime import datetime, timedelta
import numpy as np

def plot_forecast(history, forecast):
    """
    Визуализация прогноза на 30 дней (упрощенная версия)
    """
    plt.figure(figsize=(12, 6))
    
    try:
        # Получаем последнюю цену
        last_price = history['Close'].iloc[-1]
        last_date = history.index[-1]
        
        # Прогнозные значения
        forecast_values = np.array(forecast, dtype=float).flatten()
        forecast_dates = [last_date + timedelta(days=i) for i in range(1, 31)]
        
        # Простой график только прогноза
        plt.plot(forecast_dates, forecast_values, 'r-', linewidth=2, label='30-дневный прогноз')
        plt.plot(forecast_dates, forecast_values, 'ro', markersize=3)
        
        # Текущая цена как точка отсчета
        plt.axhline(y=last_price, color='blue', linestyle='--', alpha=0.7, label=f'Текущая цена (${last_price:.2f})')
        
        # Настройки
        plt.title('Прогноз цены на следующие 30 дней', fontsize=14, fontweight='bold')
        plt.xlabel('Дата')
        plt.ylabel('Цена (USD)')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:.2f}'))
        plt.tight_layout()
        
        # Сохраняем
        os.makedirs('images', exist_ok=True)
        img_path = f"images/forecast_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        plt.savefig(img_path, dpi=150, bbox_inches='tight')
        plt.close()
        
        return img_path
        
    except Exception as e:
        plt.close()
        raise Exception(f"Ошибка при построении графика: {str(e)}")