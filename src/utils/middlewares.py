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
        # Получение id пользователя.
        user_id = await backend_client.get_user_id(event.from_user.id)

        # Если пользователь не зарегистрирован,
        # отправляется предложение регистрации.
        if not user_id:
            return await event.answer(
                messages.texts.START_TEXT_FOR_NEW_USER,
                reply_markup=keyboards.RegistrationKb().add_registration()
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
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: CallbackQuery,
        data: Dict[str, Any]
    ) -> Any:
        # Пропускаем проверку, если пользователь регистрируется.
        if event.data == 'registration':
            return await handler(event, data)

        # Получение пользователя.
        user_id = await backend_client.get_user_id(event.from_user.id)

        # Если пользователь не зарегистрирован,
        # отправляется предложение регистрации.
        if not user_id:
            return await event.message.edit_text(
                messages.texts.START_TEXT_FOR_NEW_USER,
                reply_markup=keyboards.RegistrationKb().add_registration()
            )

        # Если пользователь найден, выполняется вызываемое событие.
        return await handler(event, data)
