from aiogram import Router, types
from aiogram.filters import Command

from messages.get_id_texts import PRIVATE_ID_TEXT, CHAT_ID_TEXT

router = Router()


@router.message(Command('get_id'))
async def get_id(message: types.Message):
    """Отправляет Telegram ID в приватном чате или Chat ID в групповом чате."""
    if message.from_user.id == message.chat.id:
        await message.answer(
            PRIVATE_ID_TEXT.format(telegram_id=message.from_user.id)
        )
    else:
        await message.answer(CHAT_ID_TEXT.format(chat_id=message.chat.id))
