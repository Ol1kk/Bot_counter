from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

router = Router()

@router.message(CommandStart())
async def handler_start_message(msg):
    await msg.answer("Что вы хотите сделать?")