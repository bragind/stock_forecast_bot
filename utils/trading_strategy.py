# utils/trading_strategy.py
import numpy as np

def find_local_extrema(series):
    series = np.array(series)
    buy_days = []
    sell_days = []
    for i in range(1, len(series) - 1):
        if series[i] < series[i-1] and series[i] < series[i+1]:
            buy_days.append(i)
        elif series[i] > series[i-1] and series[i] > series[i+1]:
            sell_days.append(i)
    return buy_days, sell_days

def generate_trading_recommendations(forecast, initial_amount):
    buy_days, sell_days = find_local_extrema(forecast)
    
    price_change_pct = (forecast[-1] - forecast[0]) / forecast[0] * 100

    # Простая стратегия: покупаем на первый минимум, продаём на первый максимум после него
    total_profit = 0.0
    shares = 0.0
    transactions = []

    i = j = 0
    while i < len(buy_days) and j < len(sell_days):
        buy_day = buy_days[i]
        sell_day = next((s for s in sell_days if s > buy_day), None)
        if sell_day is None:
            break
        buy_price = forecast[buy_day]
        sell_price = forecast[sell_day]
        shares = initial_amount / buy_price
        profit = shares * (sell_price - buy_price)
        total_profit += profit
        transactions.append(f"День {buy_day+1}: купите → День {sell_day+1}: продайте (прибыль: ${profit:.2f})")
        i += 1
        j = sell_days.index(sell_day) + 1

    if not transactions:
        summary = "Нет чётких сигналов для покупки/продажи."
        total_profit = 0.0
    else:
        summary = "\n".join(transactions)

    return {
        "price_change_pct": price_change_pct,
        "total_profit": total_profit,
        "summary": summary
    }