# utils/logger.py
import csv
from datetime import datetime
import os

LOG_FILE = "logs/requests.log"

os.makedirs("logs", exist_ok=True)

def log_request(user_id, ticker, amount, model_name, metric, metric_value, profit):
    with open(LOG_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if f.tell() == 0:
            writer.writerow(["user_id", "datetime", "ticker", "amount", "model", "metric", "metric_value", "profit"])
        writer.writerow([
            user_id,
            datetime.now().isoformat(),
            ticker,
            amount,
            model_name,
            metric,
            round(metric_value, 4),
            round(profit, 2)
        ])