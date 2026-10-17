from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

router = Router()

@router.callback_query(F.data == "booking:start")
async def booking(callback: CallbackQuery, state: FSMContext):
    