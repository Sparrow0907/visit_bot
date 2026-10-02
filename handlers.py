from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import Command, StateFilter

router = Router()

@router.message(Command("start"))
async def start(message: Message):
    text =("Здравствуй, мы компания 'Бьём всех'!\n"
           "Сеть тату салонов Новосибирска"
           "Что вы хотите сделать?"
           )
    await message.answer(text=text)