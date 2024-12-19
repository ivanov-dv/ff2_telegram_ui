"""Взаимодействие с бэкендом."""

from decimal import Decimal

import aiohttp
import logging

from async_lru import alru_cache
from pydantic import ValidationError

from config import AUTH_HEADERS, BACKEND_GET_USER_ID_TTL
from messages import errors
from utils.exceptions import BackendError
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

    def __init__(self, backend_url: str, headers: dict = None):
        self.backend_url = backend_url
        self.headers = headers or AUTH_HEADERS

    async def create_user(self, id_telegram: int | str) -> User:
        """
        Создание пользователя.

        :param id_telegram: Telegram ID пользователя.
        :return: User
        """
        async with aiohttp.ClientSession(headers=self.headers) as session:
            url = f'{self.backend_url}users/'
            try:
                response = await session.post(
                    url,
                    json={
                        'username': str(id_telegram),
                        'telegram_only': True,
                        'id_telegram': str(id_telegram)
                    }
                )
                return User(**(await response.json()))
            except ValidationError:
                logger.exception(f'{url=}')
                raise BackendError(errors.CREATE_USER_ERROR)
            except Exception:
                logger.exception(f'{url=}')
                raise BackendError(errors.BAСKEND_ERROR)

    @alru_cache(ttl=BACKEND_GET_USER_ID_TTL)
    async def get_user_id(self, id_telegram: str | int):
        """
        Получение ID пользователя по Telegram ID.

        :param id_telegram: Telegram ID пользователя.
        """
        async with aiohttp.ClientSession(headers=self.headers) as session:
            url = (
                f'{self.backend_url}users/'
                f'get-id/?id_telegram={id_telegram}'
            )
            try:
                response = await session.get(url)
                response_json = await response.json()
                if 'user_id' not in response_json:
                    logger.error(
                        f'{errors.BACKEND_RESPONSE_NOT_EXPECTED}\n'
                        f'{url=}\n{response_json=}'
                    )
                    raise BackendError(errors.BAСKEND_ERROR)
                return response_json['user_id']
            except Exception:
                logger.exception(f'{url=}')
                raise BackendError(errors.BAСKEND_ERROR)

    async def get_user(self, id_telegram: int | str) -> User:
        """
        Получение пользователя по Telegram ID.

        :param id_telegram: Telegram ID пользователя.
        :return: User
        """
        async with aiohttp.ClientSession(headers=self.headers) as session:
            url = f'{self.backend_url}users?id_telegram={id_telegram}'
            try:
                response = await session.get(url)
                response_json = await response.json()
                if ('results' not in response_json or
                        not response_json['results']):
                    logger.error(f'{errors.BACKEND_RESPONSE_NOT_EXPECTED}\n'
                                 f'{id_telegram=}\n{response_json=}')
                    raise BackendError(errors.BAСKEND_ERROR)
                return User(**response_json['results'][0])
            except Exception:
                logger.exception(f'{errors.BAСKEND_ERROR}\n{url=}')
                raise BackendError(errors.BAСKEND_ERROR)

    async def delete_user(self, id_telegram: int | str):
        """
        Удаление пользователя по Telegram ID

        :param id_telegram: Telegram ID пользователя.
        """
        async with aiohttp.ClientSession(headers=self.headers) as session:
            user_id = await self.get_user_id(id_telegram)
            url = f'{self.backend_url}users/{user_id}/'
            try:
                response = await session.delete(url)
                if response.status != 204:
                    logger.error(
                        f'{errors.DELETE_USER_ERROR}\n'
                        f'{response.status=}\n{await response.json()}'
                    )
                    raise BackendError(errors.DELETE_USER_ERROR)
            except Exception:
                logger.exception(f'{url=}')
                raise BackendError(errors.BAСKEND_ERROR)

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
            user_id = await self.get_user_id(id_telegram)
            url = f'{self.backend_url}users/{user_id}/summary/'
            data = {
                'type_transaction': type_transaction,
                'group_name': group_name,
                'plan_value': float(plan_value)
            }
            try:
                response = await session.post(url, json=data)
                response_json = await response.json()
                if response.status != 201:
                    logger.error(
                        f'{errors.CREATE_GROUP_ERROR}\n{url=}\n'
                        f'{data}\n{response_json=}'
                    )
                    raise BackendError(errors.CREATE_GROUP_ERROR)
                return CreatedGroup(**response_json)
            except Exception:
                logger.exception(f'{url=}')
                raise BackendError(errors.BAСKEND_ERROR)

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
        async with (aiohttp.ClientSession(headers=self.headers) as session):
            user_id = await self.get_user_id(id_telegram)
            url = (f'{self.backend_url}users/{user_id}'
                   f'summary/?group_name={group_name}')
            try:
                response = await session.get(url)
                response_json = await response.json()
                if 'summary' not in response_json:
                    logger.error(
                        f'{errors.BACKEND_RESPONSE_NOT_EXPECTED}\n{url=}'
                        f'{id_telegram=}\n{group_name=}\n{response_json=}'
                    )
                    raise BackendError(errors.BAСKEND_ERROR)
                return True if response_json['summary'] else False
            except Exception:
                logger.exception(f'{url=}')
                raise BackendError(errors.BAСKEND_ERROR)

    async def list_group(
            self,
            id_telegram: int | str,
            type_transaction: str = None
    ) -> Summary | None:
        """
        Получение списка статей.

        :param id_telegram: Telegram ID пользователя.
        :param type_transaction: Опционально. Тип транзакции.
        :return: Summary | None
        """
        async with (aiohttp.ClientSession(headers=self.headers) as session):
            user_id = await self.get_user_id(id_telegram)
            if not type_transaction:
                url = f'{self.backend_url}users/{user_id}/summary/'
            else:
                url = (
                    f'{self.backend_url}users/'
                    f'{await self.get_user_id(id_telegram)}/'
                    f'summary/?type_transaction={type_transaction}'
                )
            try:
                response = await session.get(url)
                response_json = await response.json()
                if 'summary' in response_json and not response_json['summary']:
                    return None
                return Summary(**(await response.json()))
            except ValidationError:
                logger.exception(f'{errors.LIST_GROUP_ERROR}\n{url=}')
                raise BackendError(errors.LIST_GROUP_ERROR)
            except Exception:
                logger.exception(f'{url=}')
                raise BackendError(errors.BAСKEND_ERROR)

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
            user_id = await self.get_user_id(id_telegram)
            url = f'{self.backend_url}users/{user_id}/summary/{group_id}/'
            try:
                response = await session.get(url)
                if response.status != 200:
                    logger.debug(f'{errors.GET_GROUP_ERROR}\n{url}')
                    return None
                return SummaryDetail(**(await response.json()))
            except ValidationError:
                logger.exception(f'{errors.GET_GROUP_ERROR}\n{url=}')
                raise BackendError(errors.GET_GROUP_ERROR)
            except Exception:
                logger.exception(f'{url=}')
                raise BackendError(errors.BAСKEND_ERROR)

    async def delete_group(
            self,
            id_telegram: int | str,
            group_id: int | str
    ):
        """
        Удаление статьи по Telegram ID и ID статьи.

        :param id_telegram: Telegram ID пользователя.
        :param group_id: ID статьи.
        :return: bool
        """
        async with aiohttp.ClientSession(headers=self.headers) as session:
            user_id = await self.get_user_id(id_telegram)
            url = f'{self.backend_url}users/{user_id}/summary/{group_id}/'
            try:
                response = await session.delete(url)
                if response.status != 204:
                    logger.error(
                        f'{errors.DELETE_GROUP_ERROR}\n{url=}'
                        f'{response.status=}\n{await response.json()}'
                    )
                    raise BackendError(errors.DELETE_GROUP_ERROR)
            except Exception:
                logger.exception(f'{url=}')
                raise BackendError(errors.BAСKEND_ERROR)

    async def get_summary(self, id_telegram: int | str):
        """
        Получение отчета пользователя за период,
        установленный в базовых настройках.

        :param id_telegram: Telegram ID пользователя.
        :return: Summary | None
        """
        async with aiohttp.ClientSession(headers=self.headers) as session:
            user_id = await self.get_user_id(id_telegram)
            url = f'{self.backend_url}users/{user_id}/summary/'
            try:
                response = await session.get(url)
                response_json = await response.json()
                if 'summary' in response_json and not response_json['summary']:
                    return None
                return Summary(**(await response.json()))
            except ValidationError:
                logger.exception(f'{errors.GET_SUMMARY_ERROR}\n{url=}')
                raise BackendError(errors.GET_SUMMARY_ERROR)
            except Exception:
                logger.exception(f'{url=}')
                raise BackendError(errors.BAСKEND_ERROR)

    async def add_transaction(
            self,
            id_telegram: int | str,
            type_transaction: str,
            group_name: str,
            description: str,
            value_transaction: Decimal
    ) -> Transaction:
        """
        Добавление транзакции.

        :param id_telegram: Telegram ID пользователя.
        :param type_transaction:  Тип операции.
        :param group_name: Название статьи.
        :param description: Описание.
        :param value_transaction: Значение транзакции.
        :return: Transaction
        """
        async with aiohttp.ClientSession(headers=self.headers) as session:
            user_id = await self.get_user_id(id_telegram)
            url = f'{self.backend_url}users/{user_id}/transactions/'
            data = {
                'type_transaction': type_transaction,
                'group_name': group_name,
                'description': description,
                'value_transaction': float(value_transaction)
            }
            try:
                response = await session.post(url, json=data)
                return Transaction(**(await response.json()))
            except ValidationError:
                logger.exception(
                    f'{errors.ADD_TRANSACTION_ERROR}\n{url=}'
                    f'{data=}')
                raise BackendError(errors.ADD_TRANSACTION_ERROR)
            except Exception:
                logger.exception(f'{url=}\n{data=}')
                raise BackendError(errors.BAСKEND_ERROR)

    async def update_core_settings(
            self,
            id_telegram: int | str,
            data: dict
    ) -> CoreSettingsUpdate:
        """
        Обновление core settings.

        :param id_telegram: Telegram ID пользователя.
        :param data: Новые данные (один или несколько) для core settings в виде
        {'current_space_id': 32, 'current_month': 12, 'current_year': 2024}.

        :return: CoreSettingsUpdate
        """
        async with aiohttp.ClientSession(headers=self.headers) as session:
            user_id = await self.get_user_id(id_telegram)
            url = f'{self.backend_url}users/{user_id}/core-settings/'
            try:
                response = await session.patch(url, json=data)
                return CoreSettingsUpdate(**(await response.json()))
            except ValidationError:
                logger.exception(
                    f'{errors.UPDATE_SETTINGS_ERROR}\n{url=}\n{data=}'
                )
                raise BackendError(errors.UPDATE_SETTINGS_ERROR)
            except Exception:
                logger.exception(f'{url}\n{data=}')
                raise BackendError(errors.BAСKEND_ERROR)

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
            user_id = await self.get_user_id(id_telegram)
            url = f'{self.backend_url}users/{user_id}/telegram-settings/'
            try:
                response = await session.patch(url, json=data)
                return TelegramSettings(**(await response.json()))
            except ValidationError:
                logger.exception(
                    f'{errors.UPDATE_SETTINGS_ERROR}\n{url=}\n{data=}'
                )
                raise BackendError(errors.UPDATE_SETTINGS_ERROR)
            except Exception:
                logger.exception(f'{url=}\n{data=}')
                raise BackendError(errors.BAСKEND_ERROR)

    async def update_space(
            self,
            id_telegram: int | str,
            space_id: int,
            data: dict
    ) -> Space:
        """
        Обновление пространства пользователя.

        :param id_telegram: Telegram ID пользователя.
        :param space_id: ID пространства.
        :param data: Новые данные для Space в словаре.
        :return: Space
        """
        async with aiohttp.ClientSession(headers=self.headers) as session:
            user_id = await self.get_user_id(id_telegram)
            url = f'{self.backend_url}users/{user_id}/spaces/{space_id}/'
            try:
                response = await session.patch(url, json=data)
                return Space(**(await response.json()))
            except ValidationError:
                logger.exception(
                    f'{errors.UPDATE_SETTINGS_ERROR}\n{url=}\n{data=}'
                )
                raise BackendError(errors.UPDATE_SETTINGS_ERROR)
            except Exception:
                logger.exception(f'{url=}\n{data=}')
                raise BackendError(errors.BAСKEND_ERROR)

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
        """
        async with aiohttp.ClientSession(headers=self.headers) as session:
            user_id = await self.get_user_id(id_telegram)
            url = (f'{self.backend_url}users/{user_id}/'
                   f'spaces/{id_space}/link_user/')
            data = {'id': id_link_user}
            try:
                response = await session.post(url, json=data)
                response_json = await response.json()
                if response.status != 200:
                    logger.error(
                        f'{errors.LINK_USER_ERROR}\n'
                        f'{response.status=}\n{response_json}\n{url=}\n{data=}'
                    )
                    raise BackendError(errors.LINK_USER_ERROR)
            except Exception:
                logger.exception(f'{url=}\n{data=}')
                raise BackendError(errors.BAСKEND_ERROR)

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
        """
        async with aiohttp.ClientSession(headers=self.headers) as session:
            user_id = await self.get_user_id(id_telegram)
            url = (f'{self.backend_url}users/{user_id}/'
                   f'spaces/{id_space}/unlink_user/')
            data = {'id': id_unlink_user}
            try:
                response = await session.post(url, json=data)
                if response.status != 200:
                    logger.error(
                        f'{errors.UNLINK_USER_ERROR}\n{url=}\n{data=}\n'
                        f'{response.status=}\n{await response.json()}'
                    )
                    raise BackendError(errors.UNLINK_USER_ERROR)
            except Exception as e:
                logger.exception(f'{url=}\n{data=}')
                raise BackendError(errors.BAСKEND_ERROR)
