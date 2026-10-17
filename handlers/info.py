from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, InputMediaPhoto
from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.enums import ParseMode

router = Router()

WORKS = [
    {
        "file_id": "https://picsum.photos/800/600",   # получишь, когда админ загрузит
        "title": "Рукав «Дракон»",
        "master": "Иван",
        "price": "от 15 000 ₽",
        "description": "Японский дракон на полную руку. 3–4 сеанса."
    },
    {
        "file_id": "https://picsum.photos/800/600",   # получишь, когда админ загрузит
        "title": "Что то другое",
        "master": "Своий",
        "price": "от 15 000 ₽",
        "description": "ВАЙФАЙ."
    }
]

@router.callback_query(F.data.startswith("works:"))
async def get_work(callback: CallbackQuery):
    await callback.answer()
    index = int(callback.data.removeprefix("works:"))

    total = len(WORKS)
    nav_row = []
    # Если юзер нажал старую кнопку с works:99 — сбрасываем на 0. Это защита, без неё WORKS[99]
    if not (0 <= index < total):
        index = 0

    # Стрелка "назад" — показываем, если не первый
    if index > 0:
        nav_row.append(InlineKeyboardButton(text = "←", callback_data = f"works:{index-1}"))
    if index < total - 1:
        nav_row.append(InlineKeyboardButton(text="→", callback_data = f"works:{index+1}"))
    
    rows = []
    if nav_row:
        rows.append(nav_row)
    rows.append([InlineKeyboardButton(text="← В меню", callback_data="menu")])

    work = WORKS[index]

    text = (
        f"<b>{work['title']}</b>\n\n"
        f"<i>Мастер:</i> {work['master']}\n"
        f"<i>Цена:</i> <b>{work['price']}</b>\n\n"
        f"{work['description']}\n\n"
        f"<i>{index + 1} / {total}</i>"
    )

    keyboard = InlineKeyboardMarkup(inline_keyboard=rows)

    # если у сообщения есть фото
    if callback.message.photo:
        # это то, как должно выглядеть фото
        media = InputMediaPhoto(
            media = work["file_id"], # само фото
            caption=text, # подпись к фото
            parse_mode=ParseMode.HTML
        )
        try:
            # это отправка сообщения с фото
            await callback.message.edit_media(media=media, reply_markup=keyboard)
        except TelegramBadRequest as e:
            print(f"edit_media не сработал: {e}")
    else:
        await callback.message.delete()
        await callback.message.answer_photo(
            photo=work["file_id"],
            caption=text,
            parse_mode=ParseMode.HTML,
            reply_markup=keyboard,
        )