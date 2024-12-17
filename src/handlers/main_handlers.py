import logging

from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

import messages.main_texts as main_texts
import messages.errors as errors_texts
from engine import backend_client
from messages.main_texts import get_summary_text
from messages.texts import GENERAL_DESCRIPTION
from utils import keyboards
from utils.fsm import CreateGroupState, DeleteGroupState, AddTransaction
from utils.middlewares import (
    AuthMessageMiddleware,
    AuthCallbackMiddleware
)

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
    user = await backend_client.get_user(message.from_user.id)

    # Если период не выбран, предлагает выбрать.
    if not (
        user.core_settings.current_month and user.core_settings.current_year
    ):
        await message.answer(
            main_texts.CHOOSE_PERIOD,
            reply_markup=keyboards.SettingsKb.generate_choose_period()
        )

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
            reply_markup=keyboards.WorkWithBase.main()
        )


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
    user = await backend_client.get_user(callback.from_user.id)

    # Если период не выбран, предлагает выбрать.
    if not (user.core_settings.current_month and
            user.core_settings.current_year):
        await callback.message.edit_text(
            main_texts.CHOOSE_PERIOD,
            reply_markup=keyboards.SettingsKb.generate_choose_period()
        )

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
            reply_markup=keyboards.WorkWithBase.main()
        )


@router.callback_query(F.data == 'registration')
async def add_registration(callback: types.CallbackQuery, state: FSMContext):
    """Регистрация."""

    # Очистка состояний.
    await state.clear()

    # Получение пользователя.
    # Перепроверка, если пользователь зарегистрировался на сайте.
    user = await backend_client.get_user(callback.from_user.id)

    # Если пользователь уже зарегистрирован, переходим к главному экрану.
    if user:
        await start_callback(callback, state)

    # Если пользователь не зарегистрирован, регистрируем.
    else:
        # Создание пользователя.
        user = await backend_client.create_user(callback.from_user.id)

        # Если пользователь создан успешно, отображение главного экрана.
        if user:
            user = await backend_client.get_user(callback.from_user.id)
            await callback.message.edit_text(
                main_texts.MAIN_TEXT.format(
                    first_name=callback.from_user.first_name,
                    user_id=callback.from_user.id,
                    space_name=user.core_settings.current_space.name,
                    current_month=user.core_settings.current_month,
                    current_year=user.core_settings.current_year
                ),
                reply_markup=keyboards.WorkWithBase.main()
            )

        # Если пользователь не создан, сообщение об ошибке.
        else:
            await callback.message.edit_text(errors_texts.CREATE_USER_ERROR)


@router.callback_query(F.data == 'choose_period')
async def choose_period_callback(
        callback: types.CallbackQuery,
        state: FSMContext
):
    """Выбор периода."""

    # Очистка состояний.
    await state.clear()

    # Отправка сообщения с выбором периодов.
    await callback.message.edit_text(
        main_texts.CHOOSE_PERIOD,
        reply_markup=keyboards.SettingsKb.generate_choose_period()
    )


@router.callback_query(F.data == 'settings')
async def settings_callback(callback: types.CallbackQuery, state: FSMContext):
    """Настройки."""

    # Очистка состояний.
    await state.clear()

    # Отправка сообщения с настройками.
    await callback.message.edit_text(
        main_texts.SETTINGS,
        reply_markup=keyboards.SettingsKb.settings()
    )


@router.callback_query(F.data == 'look_base')
async def look_summary(callback: types.CallbackQuery, state: FSMContext):
    """Просмотр отчета за определенный период."""

    # Очистка состояний.
    await state.clear()

    # Получение summary от бэкенда.
    summary = await backend_client.get_summary(callback.from_user.id)

    # Если summary пустое, отправка сообщения об отсутствии данных.
    if summary is None:
        await callback.message.edit_text(
            main_texts.EMPTY_SUMMARY,
            reply_markup=keyboards.WorkWithBase.main()
        )

    # Вывод отчета о summary.
    else:
        await callback.message.edit_text(
            get_summary_text(summary),
            reply_markup=keyboards.FamilyFinanceKb.go_to_main()
        )


@router.callback_query(F.data == 'create_group')
async def create_group(callback: types.CallbackQuery, state: FSMContext):
    """Создание статьи доходов или расходов."""

    # Очистка состояний.
    await state.clear()

    # Установка состояния для создания статьи.
    await state.set_state(CreateGroupState.get_type)

    # Отправка сообщения о выборе типа статьи.
    await callback.message.edit_text(
        main_texts.CREATE_GROUP,
        reply_markup=keyboards.WorkWithBase.choose_type()
    )


@router.callback_query(F.data == 'delete_group')
async def delete_group(callback: types.CallbackQuery, state: FSMContext):
    """Удаление статьи доходов или расходов."""

    # Очистка состояний.
    await state.clear()

    # Установка состояния для удаления статьи.
    await state.set_state(DeleteGroupState.get_type)

    # Отправка сообщения о выборе типа статьи.
    await callback.message.edit_text(
        main_texts.DELETE_GROUP,
        reply_markup=keyboards.WorkWithBase.choose_type()
    )


@router.callback_query(F.data == 'add_transaction')
async def add_transaction(callback: types.CallbackQuery, state: FSMContext):
    """Добавление транзакции."""

    # Очистка состояний.
    await state.clear()

    # Установка состояния для добавления транзакции.
    await state.set_state(AddTransaction.get_type)

    # Отправка сообщения о выборе типа статьи.
    await callback.message.edit_text(
        main_texts.ADD_TRANSACTION,
        reply_markup=keyboards.WorkWithBase.choose_type()
    )


@router.callback_query(F.data == 'general_description')
async def show_general_description(
        callback: types.CallbackQuery,
        state: FSMContext
):
    """Показать общее описание."""

    # Очистка состояний.
    await state.clear()

    # Отправка общего описания.
    await callback.message.edit_text(
        GENERAL_DESCRIPTION,
        reply_markup=keyboards.FamilyFinanceKb.go_to_main()
    )
