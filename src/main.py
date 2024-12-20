import asyncio
import logging

from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from engine import bot
from handlers import (
    main_handlers,
    transaction_handlers,
    registration_handlers,
    choose_period_handlers,
    settings_handlers,
    get_id_handlers,
    export_handlers
)
from messages.errors import UNEXPECTED_ERROR

logger = logging.getLogger(__name__)
dp = Dispatcher(
    storage=MemoryStorage()
)
dp.include_routers(
    main_handlers.router,
    transaction_handlers.router,
    choose_period_handlers.router,
    settings_handlers.router,
    registration_handlers.router,
    get_id_handlers.router,
    export_handlers.router
)


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except Exception as e:
        logger.exception(UNEXPECTED_ERROR.format(error=e))
