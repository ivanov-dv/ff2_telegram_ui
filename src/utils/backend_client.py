from decimal import Decimal

import aiohttp
import logging

from async_lru import alru_cache

from config import AUTH_HEADERS, BACKEND_GET_USER_ID_TTL
from utils.models import (
    User,
    Summary,
    CreatedGroup,
    SummaryDetail,
    Transaction,
    CoreSettings,
    TelegramSettings
)

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
    async def get_user_id(self, id_telegram: str | int):
        """
        Получение ID пользователя по Telegram ID.

        :param id_telegram: Telegram ID пользователя.
        :return: str | None
        """
        async with aiohttp.ClientSession(headers=self.headers) as session:
            try:
                response = await session.get(
                    f'{self.backend_url}users/'
                    f'get-id/?id_telegram={id_telegram}'
                )
                response_json = await response.json()
                if 'user_id' not in response_json:
                    logger.error('Неожиданная структура ответа сервера.')
                    return None
                return response_json['user_id']
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
                    logger.error(
                        'Неожиданная структура ответа сервера.'
                        f'{id_telegram=} {response_json=}'
                    )
                elif 'results' in response_json and response_json['results']:
                    return User(**response_json['results'][0])
                return None
            except Exception as e:
                logger.exception(e)
                return None

    async def update_user(self, id_telegram, **kwargs):
        pass

    async def create_group(
            self,
            id_telegram: int | str,
            type_transaction: str,
            group_name: str,
            plan_value: Decimal
    ) -> CreatedGroup | None:
        async with aiohttp.ClientSession(headers=self.headers) as session:
            try:
                user_id = await self.get_user_id(id_telegram)
                response = await session.post(
                    f'{self.backend_url}users/{user_id}/summary/',
                    json={
                        'type_transaction': type_transaction,
                        'group_name': group_name,
                        'plan_value': float(plan_value)
                    }
                )
                response_json = await response.json()
                if response.status != 201:
                    logger.error(
                        'Ошибка создания статьи.'
                        f'{id_telegram=} {type_transaction=} '
                        f'{group_name=} {plan_value=}'
                        f'{response_json=}'
                    )
                    return None
                return CreatedGroup(**response_json)
            except Exception as e:
                logger.exception(e)
                return None

    async def group_name_is_exist(
            self,
            id_telegram: int | str,
            group_name: str
    ):
        async with aiohttp.ClientSession(headers=self.headers) as session:
            try:
                user_id = await self.get_user_id(id_telegram)
                response = await session.get(
                    f'{self.backend_url}users/{user_id}/'
                    f'summary/?group_name={group_name}'
                )
                response_json = await response.json()
                if 'summary' not in response_json:
                    logger.error(
                        'Неожиданная структура ответа сервера.'
                        f'{id_telegram=} {group_name=} {response_json=}'
                    )
                else:
                    return (
                        True if (await response.json())['summary'] else False
                    )
            except Exception as e:
                logger.exception(e)
                return False

    async def list_group(
            self,
            id_telegram,
            type_transaction: str = None
    ) -> Summary | None:
        async with aiohttp.ClientSession(headers=self.headers) as session:
            try:
                if not type_transaction:
                    response = await session.get(
                        f'{self.backend_url}users/'
                        f'{await self.get_user_id(id_telegram)}/summary/'
                    )
                else:
                    response = await session.get(
                        f'{self.backend_url}users/'
                        f'{await self.get_user_id(id_telegram)}/'
                        f'summary/?type_transaction={type_transaction}'
                    )
                return Summary(**(await response.json()))
            except Exception as e:
                logger.exception(e)
                return None

    async def get_group(
            self,
            id_telegram: int | str,
            group_id: int | str
    ) -> SummaryDetail | None:
        async with aiohttp.ClientSession(headers=self.headers) as session:
            try:
                user_id = await self.get_user_id(id_telegram)
                response = await session.get(
                    f'{self.backend_url}users/{user_id}/summary/{group_id}/'
                )
                return SummaryDetail(**(await response.json()))
            except Exception as e:
                logger.exception(e)
                return None

    async def update_group(self, id_telegram, group_name):
        pass

    async def delete_group(self, id_telegram, group_id) -> bool:
        async with aiohttp.ClientSession(headers=self.headers) as session:
            try:
                user_id = await self.get_user_id(id_telegram)
                response = await session.delete(
                    f'{self.backend_url}users/{user_id}/summary/{group_id}/'
                )
                return response.status == 204
            except Exception as e:
                logger.exception(e)
                return False

    async def get_summary(self, id_telegram: int | str):
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

    async def add_transaction(
            self,
            id_telegram: int | str,
            type_transaction: str,
            group_name: str,
            description: str,
            value_transaction: Decimal
    ) -> Transaction | None:
        async with aiohttp.ClientSession(headers=self.headers) as session:
            try:
                user_id = await self.get_user_id(id_telegram)
                response = await session.post(
                    f'{self.backend_url}users/{user_id}/transactions/',
                    json={
                        'type_transaction': type_transaction,
                        'group_name': group_name,
                        'description': description,
                        'value_transaction': float(value_transaction)
                    }
                )
                return Transaction(**(await response.json()))
            except Exception as e:
                logger.exception(e)
                return None

    async def update_core_settings(
            self,
            id_telegram: int | str,
            core_settings: CoreSettings
    ) -> CoreSettings | None:
        async with aiohttp.ClientSession(headers=self.headers) as session:
            try:
                user_id = await self.get_user_id(id_telegram)
                response = await session.patch(
                    f'{self.backend_url}users/{user_id}/core-settings/',
                    json=core_settings.model_dump()
                )
                return CoreSettings(**(await response.json()))
            except Exception as e:
                logger.exception(e)
                return None

    async def update_telegram_settings(
            self,
            id_telegram: int | str,
            telegram_settings: TelegramSettings
    ) -> TelegramSettings | None:
        async with aiohttp.ClientSession(headers=self.headers) as session:
            try:
                user_id = await self.get_user_id(id_telegram)
                response = await session.patch(
                    f'{self.backend_url}users/{user_id}/telegram-settings/',
                    json=telegram_settings.model_dump()
                )
                return TelegramSettings(**(await response.json()))
            except Exception as e:
                logger.exception(e)
                return None
