from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
import calendar
from datetime import date
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

MONTH_NAMES = {
    1: "Январь", 2: "Февраль", 3: "Март", 4: "Апрель",
    5: "Май", 6: "Июнь", 7: "Июль", 8: "Август",
    9: "Сентябрь", 10: "Октябрь", 11: "Ноябрь", 12: "Декабрь",
}

WEEKDAYS = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]


router = Router()
                                                        # set - множество, которое удаляет повторения
def build_calendar(year: int, month: int, available_dates: set[date]) -> InlineKeyboardMarkup:
    rows: list[list[InlineKeyboardButton]] = []

    # 1. Заголовок: "Октябрь 2026"
    title = f"{MONTH_NAMES[month]} {year}"
    rows.append([InlineKeyboardButton(text=title, callback_data="noop")])

    # 2. Ряд с днями недели (только для отображения)
    rows.append([
        InlineKeyboardButton(text=wd, callback_data="noop") for wd in WEEKDAYS
    ])

    # 3. Матрица дней месяца
    month_grid = calendar.monthcalendar(year, month)

    for week in month_grid:
        row = []
        for day in week:
            if day == 0:
                # пустая ячейка (день вне месяца)
                row.append(InlineKeyboardButton(text=" ", callback_data="noop"))
                continue

            current_date = date(year, month, day)

            if current_date in available_dates:
                # есть свободные слоты
                row.append(InlineKeyboardButton(
                    text=str(day),
                    callback_data=f"booking:date:{year}-{month:02d}-{day:02d}",
                ))
            else:
                # нет слотов — точка
                row.append(InlineKeyboardButton(
                    text=f"{day}·",
                    callback_data="noop",
                ))
        rows.append(row)

    return InlineKeyboardMarkup(inline_keyboard=rows)

@router.callback_query(F.data == "noop")
async def noop(callback: CallbackQuery):
    await callback.answer()