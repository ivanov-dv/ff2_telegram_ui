"""Инициализированные экземпляры классов для работы приложения."""

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties

from config import (
    BACKEND_URL,
    AUTH_HEADERS,
    TELEGRAM_BOT_TOKEN,
    TELEGRAM_BOT_PARSE_MODE
)
from utils.backend_client import BackendClient


bot = Bot(
    token=TELEGRAM_BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=TELEGRAM_BOT_PARSE_MODE)
)
backend_client = BackendClient(BACKEND_URL, AUTH_HEADERS)
