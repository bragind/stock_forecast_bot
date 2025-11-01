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
    Визуализация исторических данных и прогноза
    
    Args:
        history: DataFrame с историческими данными или массив значений
        forecast: массив/список прогнозируемых значений
    
    Returns:
        str: путь к сохраненному изображению
    """
    plt.figure(figsize=(12, 6))
    
    try:
        # Обработка исторических данных
        if isinstance(history, pd.DataFrame):
            # Если это DataFrame с индексом datetime
            history_dates = history.index
            history_values = history['Close'].values
        else:
            # Если это массив/список значений
            history_values = np.array(history)
            history_dates = pd.date_range(
                end=datetime.now(), 
                periods=len(history_values), 
                freq='D'
            )
        
        plt.plot(history_dates, history_values, 
                label='Исторические данные', color='blue', linewidth=2)
        
        # Обработка прогноза
        forecast_values = np.array(forecast).flatten()  # Преобразуем в 1D массив
        
        # Создаем даты для прогноза
        last_historical_date = history_dates[-1] if isinstance(history, pd.DataFrame) else history_dates[-1]
        forecast_dates = [last_historical_date + timedelta(days=i) for i in range(1, len(forecast_values) + 1)]
        
        plt.plot(forecast_dates, forecast_values, 
                label='Прогноз', color='red', linestyle='--', linewidth=2, marker='o', markersize=3)
        
        # Настройки графика
        plt.title('Прогноз цены акции на 30 дней', fontsize=14, fontweight='bold')
        plt.xlabel('Дата', fontsize=12)
        plt.ylabel('Цена, USD', fontsize=12)
        plt.legend(fontsize=10)
        plt.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        
        # Форматирование осей
        plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:.2f}'))
        
        plt.tight_layout()
        
        # Сохранение
        os.makedirs('images', exist_ok=True)
        img_path = f"images/forecast_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        plt.savefig(img_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"График сохранен: {img_path}")
        print(f"История: {len(history_values)} точек, Прогноз: {len(forecast_values)} точек")
        
        return img_path
        
    except Exception as e:
        plt.close()
        raise Exception(f"Ошибка при построении графика: {str(e)}")
