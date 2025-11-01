# Телеграм-бот для прогнозирования акций

## Описание
Бот загружает данные с Yahoo Finance, обучает 3 модели (Random Forest, Prophet, LSTM), выбирает лучшую по MAPE и даёт:
- график прогноза на 30 дней,
- рекомендации по покупке/продаже,
- расчёт условной прибыли.

## Установка
```bash
pip install -r requirements.txt
python bot.py

Запуск в контейнере Docker
Скопируйте директорию на сервер

cd stock_forecast_bot 
docker build --no-cache -t stock-bot .
docker run -d --name stock-bot --env-file .env -v "${PWD}/logs:/app/logs" stock-bot
