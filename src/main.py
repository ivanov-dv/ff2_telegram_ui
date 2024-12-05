import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config import TELEGRAM_BOT_TOKEN, TELEGRAM_BOT_PARSE_MODE
# from handlers import (
#     main_handlers,
#     transaction_handlers,
#     registration_handlers,
#     choose_period_handlers,
#     settings_handlers,
#     get_id_handlers
# )
from src.messages.errors import UNEXPECTED_ERROR

logger = logging.getLogger(__name__)
bot = Bot(
    token=TELEGRAM_BOT_TOKEN,
    parse_mode=TELEGRAM_BOT_PARSE_MODE
)
dp = Dispatcher(
    storage=MemoryStorage()
)
# dp.include_routers()


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except Exception as e:
        logger.critical(UNEXPECTED_ERROR.format(error=e), exc_info=True)
