import logging
import os
import sys
from logging import StreamHandler
from logging.handlers import RotatingFileHandler

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_BOT_PARSE_MODE = 'HTML'

CONTACT_EMAIL_IN_MESSAGE = os.getenv('CONTACT_EMAIL_IN_MESSAGE', '')

# Timeout session
TIMEOUT_SESSION = 300

# ljust default for full review table
LJUST_PASS_DEFAULT = 6
LJUST_DOT_DEFAULT = 15

# Max len group name
MAX_LEN_GROUP_NAME = 15

# ID user param
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
file_handler.setLevel(logging.WARNING)

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s | %(module)s | %(funcName)s '
           '| %(levelname)s | %(message)s',
    datefmt='%Y-%m-%d | %H:%M:%S',
    handlers=[
        stream_handler,
        file_handler
    ]
)
