"""Модуль, содержащий настройки приложения."""

import logging
import os
import sys
from logging import StreamHandler
from logging.handlers import RotatingFileHandler

# Настройки телеграм бота
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_BOT_PARSE_MODE = 'HTML'

# Настройки бэкенда
BACKEND_URL = os.getenv('BACKEND_URL')
BACKEND_TOKEN = os.getenv('BACKEND_TOKEN')
AUTH_HEADERS = {'Authorization': BACKEND_TOKEN}

# Настройки glitchtip
GLITCHTIP_DSN = os.getenv('GLITCHTIP_DSN')

# Настройки кеширования
BACKEND_GET_USER_ID_TTL = 10

# Контактная почта для сообщений
CONTACT_EMAIL_IN_MESSAGE = os.getenv('CONTACT_EMAIL_IN_MESSAGE', '')

# Timeout session
TIMEOUT_SESSION = 300

# Настройки заполнения строк для отображения Summary
LJUST_PASS_DEFAULT = 6  # Макс кол-во символов в столбцах 'План' и 'Факт'
LJUST_DOT_DEFAULT = 15  # Макс кол-во символов в столбце 'Статья'

# Максимальная длина статьи
MAX_LEN_GROUP_NAME = 15

# Администраторы
ADMIN_ID = []

# Количество попыток удаления сообщений
MAX_TRY_DELETE_MSG = 3

# Таймаут между попытками удаления сообщений
TIMEOUT_TRY_DELETE_MSG = 0.5

# Настройки логирования
LOG_FOLDER = 'logs/'
LOG_MAX_SIZE_BYTES = 1024 * 1024
ROTATING_FILE_COUNT = 10
LOG_FILE_ENCODING = 'utf-8'

os.makedirs(LOG_FOLDER, exist_ok=True)
stream_handler = StreamHandler(sys.stdout)
stream_handler.setLevel(logging.DEBUG)
file_handler = RotatingFileHandler(
    filename=f'{LOG_FOLDER}'
             f'{os.path.basename(sys.modules['__main__'].__file__)[:-3]}.log',
    maxBytes=LOG_MAX_SIZE_BYTES,
    backupCount=ROTATING_FILE_COUNT,
    encoding=LOG_FILE_ENCODING,
)
file_handler.setLevel(logging.DEBUG)

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s | %(levelname)s | %(module)s | %(funcName)s '
           '| %(message)s',
    datefmt='%Y-%m-%d | %H:%M:%S',
    handlers=[
        stream_handler,
        file_handler
    ]
)
