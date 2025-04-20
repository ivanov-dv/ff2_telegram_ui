"""Хэндлеры настроек приложения."""

import logging

from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from engine import backend_client, bot
from handlers.main_handlers import start_callback
from messages import setting_texts
from messages.texts import JOINT_CHAT_INSTRUCTION, LINKED_ACCOUNTS_INSTRUCTION
from utils import keyboards as kb, keyboards
from utils.exceptions import BackendError
from utils.fsm import LinkedAccounts, JointChat, ChooseArchive

logger = logging.getLogger(__name__)
router = Router()
router.message.filter(F.chat.type.in_('private'))


@router.callback_query(F.data == 'linked_accounts')
async def manage_linked_accounts(
        callback: types.CallbackQuery,
        state: FSMContext
):
    """Управление связанными аккаунтами."""

    # Получение пользователя и запись его в состояние.
    user = await backend_client.get_user(callback.from_user.id)
    await state.update_data(user=user)

    # Проверка является ли пользователь владельцем space.
    if user.core_settings.current_space.owner_id != user.id:
        await callback.message.edit_text(
            setting_texts.NOT_OWNER_SPACE,
            reply_markup=kb.SettingsKb.back_to_settings()
        )

    # Проверка наличия доступных пользователей в текущем Space.
    elif not user.core_settings.current_space.available_linked_users:
        await callback.message.edit_text(
            setting_texts.NOT_LINKED_USERS.format(
                space_name=user.core_settings.current_space.name
            ),
            reply_markup=keyboards.SettingsKb.manage_linked_accounts()
        )

    # Если есть доступные пользователи, выводит список связанных аккаунтов.
    else:
        await callback.message.edit_text(
            setting_texts.list_linked_users(user.core_settings.current_space),
            reply_markup=keyboards.SettingsKb.manage_linked_accounts()
        )


@router.callback_query(F.data == 'linked_accounts_instruction')
async def linked_accounts_instruction(callback: types.CallbackQuery):
    """Инструкция для предоставления доступа другим пользователям."""
    await callback.message.edit_text(
        LINKED_ACCOUNTS_INSTRUCTION,
        reply_markup=kb.SettingsKb.back_to_settings()
    )


@router.callback_query(F.data == 'linked_accounts_add')
async def get_id_linked_account(
        callback: types.CallbackQuery,
        state: FSMContext
):
    """Получение ID телеграм-аккаунта для предоставления доступа."""

    # Установка состояния для получения ID телеграм-аккаунта.
    await state.set_state(LinkedAccounts.get_id_linked_account_for_add)

    # Отправка сообщения о запросе ID телеграм-аккаунта.
    msg = await callback.message.edit_text(
        setting_texts.GET_ID_FOR_LINK_USER,
        reply_markup=kb.SettingsKb.back_to_settings()
    )

    # Сохранение в состоянии номера сообщения.
    await state.update_data(msg_id=msg.message_id)


@router.message(LinkedAccounts.get_id_linked_account_for_add)
async def add_linked_account(message: types.Message, state: FSMContext):
    """Предоставления доступа."""

    # Удаление пробелов
    telegram_id_link_user = message.text.strip()

    # Проверка, существует ли подключаемый пользователь.
    link_user = await backend_client.get_user(telegram_id_link_user)

    # Получение данных из состояния.
    data = await state.get_data()

    # Если подключаемый пользователь не существует, отправка сообщения об этом.
    if not link_user:
        await message.answer(
            setting_texts.USER_NOT_REGISTERED,
            reply_markup=keyboards.SettingsKb.back_to_settings()
        )

    # Если подключаемый пользователь существует.
    else:
        # Получение пользователя из состояния.
        user = data['user']

        try:
            # Запрос на предоставление доступа пользователю.
            await backend_client.link_user_to_space(
                message.from_user.id,
                user.core_settings.current_space.id,
                link_user.id
            )

            # Отправка сообщения об успешном/неуспешном выполнении запроса.
            await message.answer(
                setting_texts.SUCCESS_LINK_USER.format(
                    id_telegram=telegram_id_link_user
                ),
                reply_markup=kb.SettingsKb.back_to_settings()
            )
        except BackendError as e:
            await message.answer(
                str(e),
                reply_markup=kb.SettingsKb.back_to_settings()
            )

    # Удаление предыдущего сообщения пользователя и бота.
    await bot.delete_message(message.from_user.id, data['msg_id'])
    await message.delete()

    # Очистка состояния.
    await state.clear()


@router.callback_query(F.data == 'linked_accounts_delete')
async def choose_delete_linked_account(
        callback: types.CallbackQuery,
        state: FSMContext
):
    """Получение данных для отзыва доступа у подключенного пользователя."""

    # Получение пользователя из состояния.
    data = await state.get_data()
    user = data['user']

    # Установка состояния для получения удаляемого пользователя.
    await state.set_state(LinkedAccounts.get_id_linked_account_for_delete)

    # Отправка сообщения для получения удаляемого пользователя.
    await callback.message.edit_text(
        setting_texts.GET_USER_FOR_UNLINK,
        reply_markup=kb.SettingsKb.generate_users_for_unlink(
            user.core_settings.current_space.available_linked_users
        )
    )


@router.callback_query(LinkedAccounts.get_id_linked_account_for_delete)
async def delete_linked_account(
        callback: types.CallbackQuery,
        state: FSMContext
):
    """Отзыв доступа."""

    # Получение удаляемого пользователя из состояния.
    data = await state.get_data()
    user = data['user']

    try:
        # Отправка запроса на отключение пользователя.
        await backend_client.unlink_user_to_space(
            callback.from_user.id,
            user.core_settings.current_space.id,
            int(callback.data)
        )
        # Отправка сообщения об успешном/неуспешном выполнении запроса.
        await callback.message.edit_text(
            setting_texts.SUCCESS_UNLINK_USER,
            reply_markup=keyboards.SettingsKb.settings()
        )

    # Отправка сообщения в случае ошибки.
    except BackendError as e:
        await callback.message.edit_text(
            str(e),
            reply_markup=keyboards.SettingsKb.settings()
        )

    # Очистка состояния.
    finally:
        await state.clear()


@router.callback_query(F.data == 'choose_space')
async def choose_base(callback: types.CallbackQuery):
    """Сообщение для выбора из доступных Spaces."""

    # Получение пользователя.
    user = await backend_client.get_user(callback.from_user.id)

    # Отправка сообщения с выбором доступных Spaces в инлайн клавиатуре.
    await callback.message.edit_text(
        setting_texts.CHOOSE_SPACE,
        reply_markup=keyboards.SettingsKb.generate_choose_space(
            user.id,
            user.spaces + user.available_linked_spaces
        )
    )


@router.callback_query(F.data.startswith('choose_space_'))
async def accept_choose_base(callback: types.CallbackQuery, state: FSMContext):
    """Обработка выбора Space."""

    # Получение идентификатора нового Space.
    new_space_id = callback.data.split('_')[2]

    try:
        # Получение пользователя.
        user = await backend_client.get_user(callback.from_user.id)

        # Проверка наличия выбранного Space в разрешенных.
        for space in user.spaces + user.available_linked_spaces:

            # Если id совпадают.
            if int(space.id) == int(new_space_id):

                # Обновление Space в core_settings текущего пользователя.
                core_settings = await backend_client.update_core_settings(
                    callback.from_user.id,
                    {'current_space_id': new_space_id}
                )

                # Если настройки успешно изменены,
                # отправляем сообщение об успешном изменении.
                if core_settings:
                    await callback.message.edit_text(
                        setting_texts.SUCCESS_UPDATE_SPACE.format(
                            space_name=space.name,
                            current_month=user.core_settings.current_month,
                            current_year=user.core_settings.current_year
                        ),
                        reply_markup=keyboards.WorkWithBase.main_menu()
                    )

                # Если настройки не были изменены, сообщение об ошибке + лог.
                else:
                    logger.error(
                        'Ошибка обновления space пользователя '
                        f'{new_space_id=} {user=}'
                    )
                    await callback.message.edit_text(
                        setting_texts.FAIL_UPDATE_SPACE,
                        reply_markup=keyboards.SettingsKb.back_to_settings()
                    )
                # Выход из цикла.
                break

    # Отправка сообщения в случае ошибки BackendError.
    except BackendError as e:
        await callback.message.edit_text(
            str(e),
            reply_markup=keyboards.SettingsKb.back_to_settings()
        )


@router.callback_query(F.data == 'joint_chat')
async def manage_joint_chat(callback: types.CallbackQuery, state: FSMContext):
    """Обработка запроса на подключение чата."""

    # Получение пользователя.
    user = await backend_client.get_user(callback.from_user.id)

    # Проверка является ли пользователь владельцем Space.
    if int(user.core_settings.current_space.owner_id) != int(user.id):

        # Если нет, выдаем сообщение об ошибке и возвращаемся в настройки.
        msg = await callback.message.edit_text(
            setting_texts.NOT_OWNER_SPACE,
            reply_markup=kb.SettingsKb.back_to_settings()
        )

    # Если чат уже подключен, выводим сообщение об этом.
    elif linked_chat := user.core_settings.current_space.linked_chat:
        msg = await callback.message.edit_text(
            setting_texts.LINKED_CHAT_CONNECTED.format(
                linked_chat=linked_chat
            ),
            reply_markup=kb.SettingsKb.joint_chat_delete()
        )

    # Если чат не подключен.
    else:
        # Установка состояния для ввода номера чата.
        await state.set_state(JointChat.get_id_joint_chat)

        # Запрос у пользователя номера чата.
        msg = await callback.message.edit_text(
            setting_texts.GET_LINKED_CHAT_ID,
            reply_markup=kb.SettingsKb.joint_chat_add()
        )

    # Сохраняем id сообщения в состоянии.
    await state.update_data(msg_id=msg.message_id)


@router.message(JointChat.get_id_joint_chat)
async def joint_chat_add(message: types.Message, state: FSMContext):
    """Добавление чата для уведомлений."""

    # Получение данных из состояния.
    data = await state.get_data()

    # Получение пользователя.
    user = await backend_client.get_user(message.from_user.id)

    # Удаление пробелов из введенного пользователем текста.
    cleaned_message = message.text.strip()

    try:
        # Отправляем запрос на изменение настроек.
        await backend_client.update_space(
            message.from_user.id,
            user.core_settings.current_space.id,
            {'linked_chat': cleaned_message}
        )

        # Если изменения успешно внесены, уведомляем пользователя.
        await message.answer(
            setting_texts.SUCCESS_LINK_CHAT.format(
                linked_chat=cleaned_message,
                current_space=user.core_settings.current_space.name,
                current_month=user.core_settings.current_month,
                current_year=user.core_settings.current_year
            ),
            reply_markup=keyboards.WorkWithBase.main_menu()
        )

    # Если изменения не внесены, уведомляем пользователя.
    except BackendError as e:
        await message.answer(
            str(e),
            reply_markup=keyboards.SettingsKb.back_to_settings()
        )

    finally:
        # Удаление предыдущих сообщений пользователя и бота.
        await bot.delete_message(message.from_user.id, data["msg_id"])
        await message.delete()

        # Очистка состояния.
        await state.clear()


@router.callback_query(F.data == 'joint_chat_delete')
async def joint_chat_delete(callback: types.CallbackQuery):
    """Обработка запроса на отключение чата."""

    # Получение пользователя.
    user = await backend_client.get_user(callback.from_user.id)

    try:
        # Отправка запроса на отключение чата.
        await backend_client.update_space(
            callback.from_user.id,
            user.core_settings.current_space.id,
            {'linked_chat': ''}
        )

        # Если изменения успешно внесены, уведомляем пользователя.
        await callback.message.edit_text(
            setting_texts.SUCCESS_DISABLE_LINK_CHAT.format(
                current_space=user.core_settings.current_space.name,
                current_month=user.core_settings.current_month,
                current_year=user.core_settings.current_year
            ),
            reply_markup=kb.WorkWithBase.main_menu()
        )

    # Если изменения не внесены, уведомляем пользователя.
    except BackendError as e:
        await callback.message.edit_text(
            str(e),
            reply_markup=keyboards.SettingsKb.back_to_settings()
        )


@router.callback_query(F.data == 'joint_chat_instruction')
async def joint_chat_instruction(callback: types.CallbackQuery):
    """Инструкция по подключению чата."""
    await callback.message.edit_text(
        JOINT_CHAT_INSTRUCTION,
        reply_markup=kb.SettingsKb().back_to_settings()
    )


@router.callback_query(F.data == 'all_periods')
async def all_periods_get_year(callback: types.CallbackQuery, state: FSMContext):
    """Выбор года."""
    # Очистка состояния.
    await state.clear()

    try:
        # Получение годов, в которых есть данные.
        years = await backend_client.get_all_years(callback.from_user.id)

        # Отправка сообщения с выбором года.
        await callback.message.edit_text(
            'Выберите год 👇\n',
            reply_markup=kb.SettingsKb.generate_choose_all_years_in_space(sorted(years, reverse=True, key=int))
        )
        await state.set_state(ChooseArchive.get_year)

    # Отправка сообщения в случае ошибки бэкенда.
    except BackendError as e:
        await callback.message.edit_text(
            str(e),
            reply_markup=keyboards.FamilyFinanceKb.go_to_main()
        )


@router.callback_query(F.data.startswith('all_periods_year_') and ChooseArchive.get_year)
async def all_periods_get_month(callback: types.CallbackQuery, state: FSMContext):
    """Выбор месяца."""

    # Сохранение года в состоянии.
    await state.update_data(year=int(callback.data.split('_')[3]))

    try:
        # Получение месяцев, в которых есть данные.
        months = await backend_client.get_all_months_in_year(callback.from_user.id, int(callback.data.split('_')[3]))

        # Отправка сообщения с выбором месяца.
        await callback.message.edit_text(
            'Выберите месяц 👇',
            reply_markup=kb.SettingsKb.generate_choose_month_in_year(sorted(months, key=int))
        )

        # Установка состояния.
        await state.set_state(ChooseArchive.get_month)

    # Отправка сообщения в случае ошибки бэкенда.
    except BackendError as e:
        await callback.message.edit_text(
            str(e),
            reply_markup=keyboards.FamilyFinanceKb.go_to_main()
        )


@router.callback_query(F.data.startswith('all_periods_month_') and ChooseArchive.get_month)
async def all_periods_set_new_period(callback: types.CallbackQuery, state: FSMContext):
    """Установка нового периода."""

    # Получение данных из состояния.
    data = await state.get_data()

    try:
        # Установка нового периода.
        await backend_client.update_core_settings(
            id_telegram=callback.from_user.id,
            data={
                'current_year': data['year'],
                'current_month': int(callback.data.split('_')[3])
            }
        )

        # Очистка состояния.
        await state.clear()

        # Переход в главное меню.
        await start_callback(callback, state)

    # Отправка сообщения в случае ошибки бэкенда.
    except BackendError as e:
        await callback.message.edit_text(
            str(e),
            reply_markup=keyboards.FamilyFinanceKb.go_to_main()
        )
