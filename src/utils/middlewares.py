"""Мидлвари."""

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message, TelegramObject
from typing import Callable, Dict, Any, Awaitable

import messages.texts
from engine import backend_client
from utils import keyboards


class AuthMessageMiddleware(BaseMiddleware):
    """
    Проверяет регистрацию пользователя при входящем событии Message.
    Если пользователь не зарегистрирован, предлагается регистрация.
    """

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        # Получение пользователя.
        user = await backend_client.get_user(event.from_user.id)

        # Если пользователь не зарегистрирован,
        # отправляется предложение регистрации.
        if not user:
            return await event.answer(
                messages.texts.START_TEXT_FOR_NEW_USER,
                reply_markup=keyboards.RegistrationKb().add_registration()
            )

        # Если space не установлено, сообщение о необходимости выбрать space.
        if user.core_settings.current_space is None:
            return await event.answer(
                messages.texts.CHOOSE_SPACE,
                reply_markup=keyboards.SettingsKb.generate_choose_period()
            )

        # Если current_month или current_year не установлены,
        # сообщение о необходимости выбрать период.
        if (user.core_settings.current_month is None or
                user.core_settings.current_year is None):
            return await event.answer(
                messages.texts.CHOOSE_PERIOD,
                reply_markup=keyboards.SettingsKb.generate_choose_period()
            )

        # Если пользователь найден, выполняется вызываемое событие.
        return await handler(event, data)


class AuthCallbackMiddleware(BaseMiddleware):
    """
    Проверяет регистрацию пользователя при входящем событии Callback.
    Если пользователь не зарегистрирован, предлагается регистрация.
    """

    async def __call__(
            self,
            handler: Callable[
                [TelegramObject, Dict[str, Any]], Awaitable[Any]
            ],
            event: CallbackQuery,
            data: Dict[str, Any]
    ) -> Any:
        # Пропускаем проверку, если пользователь регистрируется.
        if event.data == 'registration':
            return await handler(event, data)

        # Получение пользователя.
        user = await backend_client.get_user(event.from_user.id)

        # Если пользователь не зарегистрирован,
        # отправляется предложение регистрации.
        if not user:
            return await event.message.edit_text(
                messages.texts.START_TEXT_FOR_NEW_USER,
                reply_markup=keyboards.RegistrationKb().add_registration()
            )

        # Если space не установлено, сообщение о необходимости выбрать space.
        if user.core_settings.current_space is None:
            return await event.message.edit_text(
                messages.texts.CHOOSE_SPACE,
                reply_markup=keyboards.SettingsKb.generate_choose_space(
                    user.id,
                    user.spaces + user.available_linked_spaces
                )
            )

        # Если current_month или current_year не установлены,
        # сообщение о необходимости выбрать период.
        if (user.core_settings.current_month is None or
                user.core_settings.current_year is None):
            return await event.message.edit_text(
                messages.texts.CHOOSE_PERIOD,
                reply_markup=keyboards.SettingsKb.generate_choose_period()
            )

        # Если пользователь найден, выполняется вызываемое событие.
        return await handler(event, data)
