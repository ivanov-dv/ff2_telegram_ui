import logging

from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

import messages.main_texts as main_texts
import messages.errors as errors_texts
from engine import client
from utils import keyboards
from utils.middlewares import AuthMessageMiddleware, AuthCallbackMiddleware

logger = logging.getLogger(__name__)
router = Router()

# Прием сообщений ботом только в личку.
router.message.filter(F.chat.type.in_('private'))

# Мидлвари.
router.message.middleware(AuthMessageMiddleware())
router.callback_query.middleware(AuthCallbackMiddleware())


@router.message(Command('start'))
async def start(message: types.Message, state: FSMContext):
    """
    Команда /start.
    Выводит начальный экран.
    Если период не выбран, предлагает выбрать.
    """

    # Очистка состояний.
    await state.clear()

    # Получение пользователя.
    user = await client.get_user(message.from_user.id)

    # Если период не выбран, предлагает выбрать.
    if not (user.core_settings.current_month and
            user.core_settings.current_year):
        await message.answer(
            main_texts.CHOOSE_PERIOD,
            reply_markup=keyboards.SettingsKb().choose_period_list())

    # Если период выбран, выводит начальное сообщение.
    else:
        await message.answer(
            main_texts.MAIN_TEXT.format(
                first_name=message.from_user.first_name,
                user_id=message.from_user.id,
                space_name=user.core_settings.current_space.name,
                current_month=user.core_settings.current_month,
                current_year=user.core_settings.current_year
            ),
            reply_markup=keyboards.WorkWithBase().main())


@router.callback_query(F.data == 'start')
async def start_callback(callback: types.CallbackQuery, state: FSMContext):
    """
    Callback 'start'.
    Выводит начальный экран.
    Если период не выбран, предлагает выбрать.
    """

    # Очистка состояний.
    await state.clear()

    # Получение пользователя.
    user = await client.get_user(callback.from_user.id)

    # Если период не выбран, предлагает выбрать.
    if not (user.core_settings.current_month and
            user.core_settings.current_year):
        await callback.message.edit_text(
            main_texts.CHOOSE_PERIOD,
            reply_markup=keyboards.SettingsKb().choose_period_list())

    # Если период выбран, выводит начальное сообщение.
    else:
        await callback.message.edit_text(
            main_texts.MAIN_TEXT.format(
                first_name=callback.from_user.first_name,
                user_id=callback.from_user.id,
                space_name=user.core_settings.current_space.name,
                current_month=user.core_settings.current_month,
                current_year=user.core_settings.current_year
            ),
            reply_markup=keyboards.WorkWithBase().main()
        )


@router.callback_query(F.data == 'registration')
async def add_registration(callback: types.CallbackQuery, state: FSMContext):
    """Регистрация."""

    # Очистка состояний.
    await state.clear()

    # Получение пользователя.
    user = await client.create_user(callback.from_user.id)

    # Если пользователь создан успешно, отображение главного экрана.
    if user:
        user = await client.get_user(callback.from_user.id)
        await callback.message.edit_text(
            main_texts.MAIN_TEXT.format(
                first_name=callback.from_user.first_name,
                user_id=callback.from_user.id,
                space_name=user.core_settings.current_space.name,
                current_month=user.core_settings.current_month,
                current_year=user.core_settings.current_year
            ),
            reply_markup=keyboards.WorkWithBase().main()
        )

    # Если пользователь не создан, сообщение об ошибке.
    else:
        await callback.message.edit_text(
            f'{errors_texts.CREATE_USER_ERROR}'
        )


@router.callback_query(F.data == 'choose_period')
async def choose_period_callback(
        callback: types.CallbackQuery,
        state: FSMContext
):
    """Выбор периода."""

    # Очистка состояний.
    await state.clear()

    # Отправка сообщения c выбором периодов.
    await callback.message.edit_text(
        main_texts.CHOOSE_PERIOD,
        reply_markup=keyboards.SettingsKb().choose_period_list()
    )


@router.callback_query(F.data == 'settings')
async def settings_callback(callback: types.CallbackQuery, state: FSMContext):
    """Настройки."""

    # Очистка состояний.
    await state.clear()

    # Отправка сообщения с настройками.
    await callback.message.edit_text(
        main_texts.SETTINGS,
        reply_markup=keyboards.SettingsKb().settings()
    )

