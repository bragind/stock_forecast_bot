# Многоступенчатая сборка для уменьшения размера
FROM python:3.10-slim as builder

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Финальный образ
FROM python:3.10-slim

WORKDIR /app

# Копируем установленные пакеты из builder stage
COPY --from=builder /root/.local /root/.local
COPY . .

# Добавляем .local в PATH
ENV PATH=/root/.local/bin:$PATH
ENV PYTHONPATH=/app
ENV TELEGRAM_BOT_TOKEN=

RUN mkdir -p logs data

CMD ["python", "bot.py"]
