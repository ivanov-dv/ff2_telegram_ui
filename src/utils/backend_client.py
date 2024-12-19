"""Взаимодействие с бэкендом."""

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
    TelegramSettings,
    CoreSettingsUpdate,
    Space
)

logger = logging.getLogger(__name__)


class BackendClient:
    """Класс для взаимодействия с бэкендом."""

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

    async def delete_user(self, id_telegram: int | str):
        """
        Удаление пользователя по Telegram ID

        :param id_telegram: Telegram ID пользователя.
        :return: bool
        """
        async with aiohttp.ClientSession(headers=self.headers) as session:
            try:
                user_id = await self.get_user_id(id_telegram)
                response = await session.delete(
                    f'{self.backend_url}users/{user_id}/'
                )
                if response.status != 204:
                    logger.error(
                        'Ошибка удаления пользователя: '
                        f'{response.status=} {await response.json()}'
                    )
                    return False
                return True
            except Exception as e:
                logger.exception(e)

    async def create_group(
            self,
            id_telegram: int | str,
            type_transaction: str,
            group_name: str,
            plan_value: Decimal
    ) -> CreatedGroup | None:
        """
        Создание статьи.

        :param id_telegram: Telegram ID пользователя.
        :param type_transaction: Тип транзакции.
        :param group_name: Название статьи.
        :param plan_value: Плановое значение.
        :return: CreatedGroup | None
        """
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
        """
        Проверка существования статьи по имени.

        :param id_telegram: Telegram ID пользователя.
        :param group_name: Название статьи.
        :return: Bool
        """
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
        """
        Получение списка статей.

        :param id_telegram: Telegram ID пользователя.
        :param type_transaction: Опционально. Тип транзакции.
        :return: Summary | None
        """
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
        """
        Получение детальной информации о статье.

        :param id_telegram: Telegram ID пользователя.
        :param group_id: ID статьи.
        :return: SummaryDetail | None
        """
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

    async def delete_group(
            self,
            id_telegram: int | str,
            group_id: int | str
    ) -> bool:
        """
        Удаление статьи по Telegram ID и ID статьи.

        :param id_telegram: Telegram ID пользователя.
        :param group_id: ID статьи.
        :return: bool
        """
        async with aiohttp.ClientSession(headers=self.headers) as session:
            try:
                user_id = await self.get_user_id(id_telegram)
                response = await session.delete(
                    f'{self.backend_url}users/{user_id}/summary/{group_id}/'
                )
                if response.status != 204:
                    logger.error(
                        'Ошибка удаления статьи: '
                        f'{response.status=} {await response.json()}'
                    )
                    return False
                return True
            except Exception as e:
                logger.exception(e)
                return False

    async def get_summary(self, id_telegram: int | str):
        """
        Получение отчета пользователя за период,
        установленный в базовых настройках.

        :param id_telegram: Telegram ID пользователя.
        :return: Summary | None
        """
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
        """
        Добавление транзакции.

        :param id_telegram: Telegram ID пользователя.
        :param type_transaction:  Тип операции.
        :param group_name: Название статьи.
        :param description: Описание.
        :param value_transaction: Значение транзакции.
        :return: Transaction | None
        """
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
            data: dict
    ) -> CoreSettingsUpdate | None:
        """
        Обновление core settings.

        :param id_telegram: Telegram ID пользователя.
        :param data: Новые данные (один или несколько) для core settings в виде
        {'current_space_id': 32, 'current_month': 12, 'current_year': 2024}.

        :return: CoreSettingsUpdate | None
        """
        async with aiohttp.ClientSession(headers=self.headers) as session:
            try:
                user_id = await self.get_user_id(id_telegram)
                response = await session.patch(
                    f'{self.backend_url}users/{user_id}/core-settings/',
                    json=data
                )
                return CoreSettingsUpdate(**(await response.json()))
            except Exception as e:
                logger.exception(e)
                return None

    async def update_telegram_settings(
            self,
            id_telegram: int | str,
            data: dict
    ) -> TelegramSettings | None:
        """
        Обновление Telegram settings.

        :param id_telegram: Telegram ID пользователя.
        :param data: Новые данные для Telegram settings в словаре.
        :return: TelegramSettings | None
        """
        async with aiohttp.ClientSession(headers=self.headers) as session:
            try:
                user_id = await self.get_user_id(id_telegram)
                response = await session.patch(
                    f'{self.backend_url}users/{user_id}/telegram-settings/',
                    json=data
                )
                return TelegramSettings(**(await response.json()))
            except Exception as e:
                logger.exception(e)
                return None

    async def update_space(
            self,
            id_telegram: int | str,
            space_id: int,
            data: dict
    ) -> Space | None:
        """
        Обновление пространства пользователя.

        :param id_telegram: Telegram ID пользователя.
        :param space_id: ID пространства.
        :param data: Новые данные для Space в словаре.
        :return: Space | None
        """
        async with aiohttp.ClientSession(headers=self.headers) as session:
            try:
                user_id = await self.get_user_id(id_telegram)
                response = await session.patch(
                    f'{self.backend_url}users/{user_id}/spaces/{space_id}/',
                    json=data
                )
                return Space(**(await response.json()))
            except Exception as e:
                logger.exception(e)
                return None

    async def link_user_to_space(
            self,
            id_telegram: int | str,
            id_space: int | str,
            id_link_user: int | str
    ):
        """
        Связывание пользователя с пространством.

        :param id_telegram: Telegram ID пользователя.
        :param id_space: ID пространства.
        :param id_link_user: ID пользователя для связывания.
        :return: Bool
        """
        async with aiohttp.ClientSession(headers=self.headers) as session:
            try:
                user_id = await self.get_user_id(id_telegram)
                response = await session.post(
                    f'{self.backend_url}users/{user_id}/'
                    f'spaces/{id_space}/link_user/',
                    json={'id': id_link_user}
                )
                if response.status != 200:
                    logger.error(
                        f'Ошибка при связывании пользователя с пространством: '
                        f'{response.status=} {await response.json()}'
                    )
                    return False
                return response.status == 200
            except Exception as e:
                logger.exception(e)
                return False

    async def unlink_user_to_space(
            self,
            id_telegram: int | str,
            id_space: int | str,
            id_unlink_user: int | str
    ):
        """
        Отключение пользователя от пространства.

        :param id_telegram: Telegram ID пользователя.
        :param id_space: ID пространства.
        :param id_unlink_user: ID пользователя для отключения.
        :return: Bool
        """
        async with aiohttp.ClientSession(headers=self.headers) as session:
            try:
                user_id = await self.get_user_id(id_telegram)
                response = await session.post(
                    f'{self.backend_url}users/{user_id}/'
                    f'spaces/{id_space}/unlink_user/',
                    json={'id': id_unlink_user}
                )
                if response.status != 200:
                    logger.error(
                        f'Ошибка при отвязке пользователя от пространства: '
                        f'{response.status=} {await response.json()}'
                    )
                    return False
                return True
            except Exception as e:
                logger.exception(e)
                return False
