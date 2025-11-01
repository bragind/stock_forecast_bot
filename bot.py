# bot.py
import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import FSInputFile

from utils.data_loader import load_stock_data
from models.model_selector import select_best_model
from utils.visualizer import plot_forecast
from utils.trading_strategy import generate_trading_recommendations
from utils.logger import log_request

# Загрузка переменных окружения (для локальной разработки)
from dotenv import load_dotenv
load_dotenv()

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Получение токена из переменной окружения
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("Токен Telegram-бота не задан. Установите переменную окружения TELEGRAM_BOT_TOKEN.")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

class StockRequest(StatesGroup):
    ticker = State()
    amount = State()

@dp.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    await message.answer("Привет! 📈 Введите тикер акции (AAPL, MSFT, TSLA и т.д.):")
    await state.set_state(StockRequest.ticker)

@dp.message(StockRequest.ticker)
async def process_ticker(message: types.Message, state: FSMContext):
    ticker = message.text.strip().upper()
    if not ticker:
        await message.answer("Пожалуйста, введите корректный тикер.")
        return

    try:
        df = load_stock_data(ticker)
        await state.update_data(ticker=ticker, df=df)
        await message.answer("Введите сумму инвестиции (в USD):")
        await state.set_state(StockRequest.amount)
    except Exception as e:
        await message.answer(f"❌ Ошибка при загрузке данных для {ticker}:\n{e}\n\nПопробуйте другой тикер (например, AAPL).")
        await state.clear()

@dp.message(StockRequest.amount)
async def process_amount(message: types.Message, state: FSMContext):
    logging.info("Начало обработки суммы")
    try:
        amount = float(message.text.strip())
        if amount <= 0:
            raise ValueError("Сумма должна быть положительной.")
    except ValueError:
        await message.answer("Пожалуйста, введите корректное положительное число (например, 1000).")
        return

    user_data = await state.get_data()
    ticker = user_data.get("ticker")
    df = user_data.get("df")

    if df is None or ticker is None:
        await message.answer("Произошёл сбой: данные не найдены. Начните сначала командой /start.")
        await state.clear()
        return

    await message.answer("⏳ Анализирую данные и строю прогноз... Это может занять 1–2 минуты.")
    logging.info(f"Загружены данные для {ticker}, сумма: {amount}")

    try:
        best_model_info = select_best_model(df)
        logging.info("Модель выбрана")

        forecast = best_model_info["forecast"]
        model_name = best_model_info["model_name"]
        metric_value = best_model_info["metric_value"]
        logging.info(f"Прогноз длиной {len(forecast)} дней")

        img_path = plot_forecast(df, forecast)
        logging.info(f"График сохранён: {img_path}")

        recommendations = generate_trading_recommendations(forecast, amount)
        logging.info("Рекомендации сформированы")

        log_request(
            user_id=message.from_user.id,
            ticker=ticker,
            amount=amount,
            model_name=model_name,
            metric="MAPE",
            metric_value=metric_value,
            profit=recommendations["total_profit"]
        )
        logging.info("Запрос залогирован")

        await message.answer_photo(
            photo=FSInputFile(img_path),
            caption=(
                f"📈 Прогноз на 30 дней по акции {ticker}\n"
                f"Изменение цены: {recommendations['price_change_pct']:.2f}%\n\n"
                f"🔍 Рекомендации:\n{recommendations['summary']}\n\n"
                f"💰 Потенциальная прибыль: ${recommendations['total_profit']:.2f}"
            )
        )
        logging.info("Ответ отправлен пользователю")

    except Exception as e:
        logging.exception("Критическая ошибка при прогнозировании")
        error_msg = str(e)
        if "Close" in error_msg or "KeyError" in error_msg or "empty" in error_msg.lower():
            await message.answer(
                "❌ Не удалось обработать тикер. Возможные причины:\n"
                "• Тикер не существует (попробуйте AAPL, MSFT, TSLA);\n"
                "• Нет исторических данных;\n"
                "• Это индекс или ETF, который не поддерживается.\n\n"
                "Попробуйте другой тикер."
            )
        else:
            await message.answer(f"❌ Произошла ошибка при прогнозировании:\n{error_msg}")
    finally:
        await state.clear()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())