import os
import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from datetime import date, datetime

from telegram_calendar.builder import build_year_selector, build_month_selector, build_calendar
from telegram_calendar.callback import CalendarCallback

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("Переменная окружения BOT_TOKEN не установлена")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

def get_icon_dates(user_id: int, year: int, month: int):
    return {
        date(year, month, 1).strftime("%Y-%m-%d"): "💼",
        date(year, month, 5).strftime("%Y-%m-%d"): "🎉",
        date(year, month, 8).strftime("%Y-%m-%d"): "🔥"
    }

@dp.message(Command("start"))
async def cmd_start(msg: Message):
    today = datetime.today()
    await msg.answer("Выберите год:", reply_markup=build_year_selector(today.year))

@dp.callback_query(CalendarCallback.filter(F.action == "show_years"))
async def on_show_years(callback: CallbackQuery, callback_data: CalendarCallback):
    kb = build_year_selector(callback_data.year)
    await callback.message.edit_text("Выберите год:", reply_markup=kb)
    await callback.answer()

@dp.callback_query(CalendarCallback.filter(F.action == "change_year_range"))
async def on_change_year_range(callback: CallbackQuery, callback_data: CalendarCallback):
    kb = build_year_selector(callback_data.year)
    await callback.message.edit_text("Выберите год:", reply_markup=kb)
    await callback.answer()

@dp.callback_query(CalendarCallback.filter(F.action == "select_year"))
async def on_year(callback: CallbackQuery, callback_data: CalendarCallback):
    # При выборе года показываем месяцы этого года
    await callback.message.edit_text("Выберите месяц:", reply_markup=build_month_selector(callback_data.year))
    await callback.answer()

@dp.callback_query(CalendarCallback.filter(F.action == "show_months"))
async def on_show_months(callback: CallbackQuery, callback_data: CalendarCallback):
    # При клике на заголовок месяца показываем выбор месяцев текущего года
    await callback.message.edit_text("Выберите месяц:", reply_markup=build_month_selector(callback_data.year))
    await callback.answer()

@dp.callback_query(CalendarCallback.filter(F.action == "select_month"))
async def on_month(callback: CallbackQuery, callback_data: CalendarCallback):
    icons = get_icon_dates(callback.from_user.id, callback_data.year, callback_data.month)
    cal = build_calendar(callback_data.year, callback_data.month, icons)
    await callback.message.edit_text(f"Календарь на {callback_data.month:02}.{callback_data.year}:", reply_markup=cal)
    await callback.answer()

@dp.callback_query(CalendarCallback.filter(F.action == "select_day"))
async def on_day(callback: CallbackQuery, callback_data: CalendarCallback):
    await callback.message.answer(f"Вы выбрали дату: <b>{callback_data.day:02}.{callback_data.month:02}.{callback_data.year}</b>", parse_mode="HTML")
    await callback.answer()


@dp.callback_query(F.data == "ignore")
async def ignore_callback(callback: CallbackQuery):
    await callback.answer()


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
