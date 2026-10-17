from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, InputMediaPhoto
from aiogram.exceptions import TelegramBadRequest
from aiogram.enums import ParseMode



text_menu_kb = (
        "Здравствуйте! Мы — сеть тату-салонов «Бьём всех» в Новосибирске.\n\n"
        "Что хотите сделать?"
    )

def menu_keyboard():
    return InlineKeyboardMarkup(
                        inline_keyboard=[
                            [
                        InlineKeyboardButton(text="О нас.", callback_data="info"),
                        InlineKeyboardButton(text="Наши работы.", callback_data='works:0')             
                            ], 
                        [
                        InlineKeyboardButton(text="Сделать бронь", callback_data="booking:start")
                        ]
                                        ])

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()  # на случай, если юзер был в середине брони


    await message.answer(text_menu_kb, reply_markup=menu_keyboard)



@router.callback_query(F.data == "menu")
async def get_menu(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.answer()

    # Если предыдущее сообщение - фото, то делаем так
    if callback.message.photo:
        await callback.message.delete()
        await callback.message.answer(text=text_menu_kb, reply_markup=menu_keyboard)
    else:
        # если предыдущее - текст
        await callback.message.edit_text(text_menu_kb, reply_markup=menu_keyboard)