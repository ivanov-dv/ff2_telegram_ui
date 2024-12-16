import aiohttp
import logging

from async_lru import alru_cache

from config import AUTH_HEADERS, BACKEND_GET_USER_ID_TTL
from utils.models import User, Summary

logger = logging.getLogger(__name__)


class BackendClient:
    def __init__(self, backend_url: str, token: str, headers: dict = None):
        self.backend_url = backend_url
        self.token = token
        self.headers = headers or AUTH_HEADERS

    async def create_user(self, id_telegram: int | str) -> User | None:
        """
        Создание пользователя.

        :param id_telegram: Telegram ID пользователя.
        :return: User | None
        """
        async with aiohttp.ClientSession(headers=self.headers) as session:
            try:
                response = await session.post(
                    f'{self.backend_url}users/',
                    json={
                        'username': str(id_telegram),
                        'telegram_only': True,
                        'id_telegram': str(id_telegram)
                    }
                )
                return User(**(await response.json()))
            except Exception as e:
                logger.exception(e)
                return None

    @alru_cache(ttl=BACKEND_GET_USER_ID_TTL)
    async def get_user_id(self, id_telegram):
        """
        Получение ID пользователя по Telegram ID.

        :param id_telegram: Telegram ID пользователя.
        :return: str | None
        """
        async with aiohttp.ClientSession(headers=self.headers) as session:
            try:
                response = await session.get(
                    f'{self.backend_url}users/'
                    f'get-id/?telegram_id={id_telegram}'
                )
                response_json = await response.json()
                if 'id' not in response_json:
                    logger.error('Неожиданная структура ответа сервера.')
                    return None
                return response_json['id']
            except Exception as e:
                logger.exception(e)
                return None

    async def get_user(self, id_telegram: int | str) -> User | None:
        """
        Получение пользователя по Telegram ID.

        :param id_telegram: Telegram ID пользователя.
        :return: User | None
        """
        async with aiohttp.ClientSession(headers=self.headers) as session:
            try:
                response = await session.get(
                    f'{self.backend_url}users?id_telegram={id_telegram}'
                )
                response_json = await response.json()
                if 'results' not in response_json:
                    logger.error('Неожиданная структура ответа сервера.')
                elif 'results' in response_json and response_json['results']:
                    return User(**response_json['results'][0])
                return None
            except Exception as e:
                logger.exception(e)
                return None

    async def update_user(self, id_telegram, **kwargs):
        pass

    async def create_group(self, id_telegram, group_name):
        pass

    async def get_group(self, id_telegram, group_name):
        pass

    async def update_group(self, id_telegram, group_name):
        pass

    async def delete_group(self, id_telegram, group_name):
        pass

    async def get_summary(self, id_telegram):
        async with aiohttp.ClientSession(headers=self.headers) as session:
            try:
                user_id = await self.get_user_id(id_telegram)
                if not user_id:
                    return None
                response = await session.get(
                    f'{self.backend_url}users/{user_id}/summary/'
                )
                response_json = await response.json()
                if not response_json.get('summary'):
                    return None
                return Summary(**(await response.json()))
            except Exception as e:
                logger.exception(e)
                return None

    async def add_transaction(self, id_telegram, transaction):
        pass
