"""Хэндлеры выполнения транзакций."""

from decimal import Decimal

from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext

from engine import backend_client, bot
from messages import transaction_texts
from utils.exceptions import BackendError
from utils.fsm import (
    CreateGroupState,
    DeleteGroupState,
    AddTransaction
)
from utils import keyboards
from utils.validators import validate_group_name, validate_digit_value

router = Router()
router.message.filter(F.chat.type.in_('private'))


@router.callback_query(CreateGroupState.get_type)
async def create_group_get_type(
        callback: types.CallbackQuery,
        state: FSMContext
):
    """Получение типа статьи и запрос названия."""

    # Запись в состоянии выбранный тип статьи.
    await state.update_data(type=callback.data)

    # Установка состояния для получения имени статьи.
    await state.set_state(CreateGroupState.get_name)

    # Отправка сообщения о вводе названия статьи.
    msg = await callback.message.edit_text(
        transaction_texts.GET_NAME_FOR_CREATE_GROUP,
        reply_markup=keyboards.FamilyFinanceKb.go_to_main()
    )

    # Сохранение в состоянии номера сообщения.
    await state.update_data(msg_id=msg.message_id)


@router.message(CreateGroupState.get_name)
async def create_group_get_name(message: types.Message, state: FSMContext):
    """Получение, валидация названия статьи и запрос планового значения."""

    # Получение данных из state.
    data = await state.get_data()

    try:
        # Валидация названия статьи.
        validated_group_name, error_message = validate_group_name(message.text)

        # Отправка сообщения об ошибке.
        if error_message:
            msg = await message.answer(
                error_message,
                reply_markup=keyboards.FamilyFinanceKb.go_to_main()
            )


        # Если ошибка не обнаружена, проверка на уникальность названия статьи.
        elif await backend_client.group_name_is_exist(
                message.from_user.id,
                validated_group_name
        ):
            msg = await message.answer(
                transaction_texts.GROUP_NAME_IS_EXIST,
                reply_markup=keyboards.FamilyFinanceKb.go_to_main()
            )

        # Если название статьи уникальное, отправка сообщения о создании статьи.
        else:
            # Установка состояния для получения планового значения статьи.
            await state.set_state(CreateGroupState.get_plan_value)

            # Сохранение названия статьи в состоянии.
            await state.update_data(group_name=validated_group_name)

            # Отправка сообщения о вводе планового значения статьи.
            msg = await message.answer(
                transaction_texts.GET_PLAN_VALUE_FOR_CREATE_GROUP.format(
                    group_name=validated_group_name
                ),
                reply_markup=keyboards.FamilyFinanceKb.go_to_main()
            )

    # Отправка сообщения в случае ошибки.
    except BackendError as e:
        msg = await message.answer(
            str(e),
            reply_markup=keyboards.FamilyFinanceKb.go_to_main()
        )

    finally:
        # Удаление предыдущего сообщения пользователя.
        await message.delete()

        # Удаление предыдущего сообщения бота.
        await bot.delete_message(message.from_user.id, data['msg_id'])

        # Сохранение в состоянии номера сообщения.
        await state.update_data(msg_id=msg.message_id)


@router.message(CreateGroupState.get_plan_value)
async def create_group_get_plan_value(
        message: types.Message,
        state: FSMContext
):
    """Получение, валидация планового значения и создание новой статьи."""

    # Получение данных из state.
    data = await state.get_data()

    try:
        # Валидация планового значения.
        validated_value, error_message = validate_digit_value(message.text)

        # Если значение не валидно, отправка сообщения об ошибке.
        if error_message:
            msg = await message.answer(
                error_message,
                reply_markup=keyboards.FamilyFinanceKb.go_to_main()
            )
            await state.update_data(msg_id=msg.message_id)

        # Если значение валидно, создание новой статьи.
        else:
            # Запрос на создание статьи.
            new_group = await backend_client.create_group(
                message.from_user.id,
                data['type'],
                data['group_name'],
                Decimal(str(validated_value))
            )

            # Если статья создана, отправка сообщения о создании статьи.
            if new_group:
                type_value = 'Доход' if data['type'] == 'income' else 'Расход'
                await message.answer(
                    transaction_texts.SUCCESS_CREATE_GROUP.format(
                        group_name=data['group_name'],
                        type_value=type_value,
                        value=round(validated_value / 1000, 3)
                    ),
                    reply_markup=keyboards.WorkWithBase.main_menu()
                )

                # Получение настроек пользователя.
                user = await backend_client.get_user(message.from_user.id)

                # Если есть чат для совместной работы,
                # отправка сообщения в него.
                if user.core_settings.current_space.linked_chat:
                    await bot.send_message(
                        user.core_settings.current_space.linked_chat,
                        transaction_texts.NOTICE_TO_JOINT_CHAT_CREATE_GROUP.
                        format(
                            first_name=message.from_user.first_name,
                            telegram_id=message.from_user.id,
                            current_space=user.
                                core_settings.current_space.name,
                            current_month=user.core_settings.current_month,
                            current_year=user.core_settings.current_year,
                            type_value=type_value,
                            group_name=data['group_name'],
                            plan_value=round(validated_value / 1000, 3)
                        )
                    )

    # Если статья не создана, отправка сообщения об ошибке.
    except BackendError as e:
        await message.answer(
            str(e),
            reply_markup=keyboards.FamilyFinanceKb.go_to_main()
        )

    finally:
        # Очистка состояний.
        await state.clear()

        # Удаление предыдущего сообщения пользователя.
        await message.delete()

        # Удаление предыдущего сообщения бота.
        await bot.delete_message(message.from_user.id, data['msg_id'])


@router.callback_query(DeleteGroupState.get_type)
async def delete_group_get_type(
        callback: types.CallbackQuery,
        state: FSMContext
):
    """
    Получение типа статьи для удаления
    и запрос имени статьи через инлайн кнопки.
    """

    try:
        # Получение списка статей по типу.
        summary = await backend_client.list_group(
            callback.from_user.id,
            callback.data
        )

        # Если статей нет, отправка сообщения об этом.
        if not summary.summary:
            await callback.message.edit_text(
                transaction_texts.GROUPS_NOT_EXIST,
                reply_markup=keyboards.FamilyFinanceKb.go_to_main()
            )

        # Если статьи есть, отправка сообщения о выборе статьи.
        else:
            # Запись типа статьи в состояние.
            await state.update_data(type=callback.data)

            # Установка состояния для получения имени статьи.
            await state.set_state(DeleteGroupState.get_name)

            # Отправка сообщения о выборе имени статьи.
            await callback.message.edit_text(
                transaction_texts.GET_NAME_FOR_DELETE_GROUP,
                reply_markup=keyboards.WorkWithBase.choose_group_name(summary)
            )
    except BackendError as e:
        await callback.message.edit_text(
            str(e),
            reply_markup=keyboards.FamilyFinanceKb.go_to_main()
        )


@router.callback_query(DeleteGroupState.get_name)
async def delete_group_get_name(callback: types.CallbackQuery,
                                state: FSMContext):
    """Получение имени статьи и её удаление."""

    # Получение данных из состояния.
    data = await state.get_data()

    # Получение id статьи из callback-кнопки.
    group_id = callback.data.split('_')[2]

    try:
        # Получение данных статьи по id.
        group = await backend_client.get_group(
            callback.from_user.id,
            group_id
        )

        # Если статья удалена корректно
        if await backend_client.delete_group(
            callback.from_user.id,
            group_id
        ):

            # Человекочитаемый тип статьи.
            type_value = 'Доход' if data['type'] == 'income' else 'Расход'

            # Отправка сообщения об успешном удалении статьи.
            await callback.message.edit_text(
                transaction_texts.SUCCESS_DELETE_GROUP.format(
                    group_name=group.group_name,
                    type_value=type_value
                ),
                reply_markup=keyboards.WorkWithBase.main_menu()
            )

            # Получение данных о пользователе.
            user = await backend_client.get_user(callback.from_user.id)

            # Если есть чат для совместной работы, отправка сообщения в него.
            if user.core_settings.current_space.linked_chat:
                await bot.send_message(
                    user.core_settings.current_space.linked_chat,
                    transaction_texts.NOTICE_TO_JOINT_CHAT_DELETE_GROUP.format(
                        first_name=callback.from_user.first_name,
                        telegram_id=callback.from_user.id,
                        current_space=user.core_settings.current_space.name,
                        current_month=user.core_settings.current_month,
                        current_year=user.core_settings.current_year,
                        type_value=type_value,
                        group_name=group.group_name
                    )
                )

    # Отправка сообщения в случае ошибки.
    except BackendError as e:
        await callback.message.edit_text(
            str(e),
            reply_markup=keyboards.FamilyFinanceKb.go_to_main()
        )


@router.callback_query(AddTransaction.get_type)
async def add_transaction_get_type(
        callback: types.CallbackQuery,
        state: FSMContext
):
    """Получение типа для добавления транзакции и запрос статьи."""

    try:
        # Получение статей по типу.
        summary = await backend_client.list_group(
            callback.from_user.id,
            callback.data
        )

        # Если статей нет, отправляется сообщение об этом.
        if not summary.summary:
            await callback.message.edit_text(
                transaction_texts.GROUPS_NOT_EXIST,
                reply_markup=keyboards.FamilyFinanceKb.go_to_main()
            )

        # Если статьи есть.
        else:
            # Сохранение типа в состояние.
            await state.update_data(type=callback.data)

            # Установка состояния для получения статьи.
            await state.set_state(AddTransaction.get_group)

            # Отправка сообщения для выбора статьи.
            await callback.message.edit_text(
                transaction_texts.GET_GROUP_ADD_TRANSACTION,
                reply_markup=keyboards.WorkWithBase.choose_group_name(summary)
            )
    # Отправка сообщения в случае ошибки.
    except BackendError as e:
        await callback.message.edit_text(
            str(e),
            reply_markup=keyboards.FamilyFinanceKb.go_to_main()
        )


@router.callback_query(AddTransaction.get_group)
async def add_transaction_get_group(
        callback: types.CallbackQuery,
        state: FSMContext
):
    """Получение статьи и запрос значения транзакции."""

    # Получение id статьи и запись в состояние.
    group_id = callback.data.split('_')[2]
    await state.update_data(group_id=group_id)

    # Получение статьи и её запись имени в состояние.
    group = await backend_client.get_group(
        callback.from_user.id,
        group_id
    )
    await state.update_data(group_name=group.group_name)

    # Установка состояния для получения значения транзакции.
    await state.set_state(AddTransaction.get_value)

    # Отправка сообщения для получения значения транзакции.
    msg = await callback.message.edit_text(
        transaction_texts.GET_VALUE_ADD_TRANSACTION.format(
            group_name=group.group_name
        ),
        reply_markup=keyboards.FamilyFinanceKb.go_to_main())

    # Запись ID сообщения в состояние.
    await state.update_data(msg_id=msg.message_id)


@router.message(AddTransaction.get_value)
async def add_transaction_get_value(message: types.Message, state: FSMContext):
    """Получение значения транзакции и запрос описания."""

    # Получение данных из состояния.
    data = await state.get_data()

    try:
        # Валидация введенного значения.
        validated_value, error_message = validate_digit_value(message.text)

        # Если значение не валидно, отправка сообщения об ошибке.
        if error_message:
            msg = await message.answer(
                error_message,
                reply_markup=keyboards.FamilyFinanceKb.go_to_main()
            )

        # Если значение валидно.
        else:
            # Запись введенного значения в состояние.
            await state.update_data(value=validated_value)

            # Установка состояния для получения описания транзакции.
            await state.set_state(AddTransaction.get_description)

            # Отправка сообщения для получения описания транзакции.
            msg = await message.answer(
                transaction_texts.GET_DESCRIPTION_ADD_TRANSACTION,
                reply_markup=keyboards.FamilyFinanceKb.go_to_main()
            )

    # Отправка сообщения в случае ошибки.
    except BackendError as e:
        msg = await message.answer(
            str(e),
            reply_markup=keyboards.FamilyFinanceKb.go_to_main()
        )

    finally:
        # Удаление предыдущего сообщения пользователя.
        await message.delete()

        # Удаление предыдущего сообщения бота.
        await bot.delete_message(message.from_user.id, data['msg_id'])

        # Запись ID нового сообщения в состояние.
        await state.update_data(msg_id=msg.message_id)


@router.message(AddTransaction.get_description)
async def add_transaction_get_description(
        message: types.Message,
        state: FSMContext
):
    """Получение описания транзакции и сохранение."""

    # Получение данных из состояния.
    data = await state.get_data()

    try:
        # Получение текущей записи статьи.
        old_group = await backend_client.get_group(
            message.from_user.id,
            data['group_id']
        )

        # Сохранение новой транзакции.
        transaction = await backend_client.add_transaction(
            message.from_user.id,
            data['type'],
            data['group_name'],
            message.text,
            Decimal(str(data['value']))
        )

        # Человекочитаемый тип статьи.
        type_transaction = 'Доход' if data['type'] == 'income' else 'Расход'

        # Получение данных о пользователе.
        user = await backend_client.get_user(message.from_user.id)

        # Отправка сообщения об успешном добавлении транзакции.
        await message.answer(
            transaction_texts.SUCCESS_ADD_TRANSACTION.format(
                current_month=user.core_settings.current_month,
                current_year=user.core_settings.current_year,
                type_transaction=type_transaction,
                group_name=data['group_name'],
                old_value=round(old_group.fact_value / 1000, 2),
                new_value=round(transaction.value_transaction / 1000, 2),
                description=transaction.description
            ),
            reply_markup=keyboards.WorkWithBase.main_menu()
        )

        # Если есть чат для совместной работы, отправка сообщения в него.
        if user.core_settings.current_space.linked_chat:
            await bot.send_message(
                user.core_settings.current_space.linked_chat,
                transaction_texts.NOTICE_TO_JOINT_CHAT_ADD_TRANSACTION.format(
                    first_name=message.from_user.first_name,
                    id_telegram=message.from_user.id,
                    current_space=user.core_settings.current_space.name,
                    current_month=user.core_settings.current_month,
                    current_year=user.core_settings.current_year,
                    type_transaction=type_transaction,
                    group_name=data['group_name'],
                    value_transaction=round(
                        transaction.value_transaction / 1000, 2
                    ),
                    description=transaction.description
                )
            )

    # Если транзакция не сохранена, отправка сообщения об ошибке.
    except BackendError as e:
        await message.answer(
            str(e),
            reply_markup=keyboards.FamilyFinanceKb.go_to_main()
        )

    finally:
        # Удаление предыдущего сообщения пользователя.
        await message.delete()

        # Удаление предыдущего сообщения бота.
        await bot.delete_message(message.from_user.id, data['msg_id'])

        # Очистка состояния.
        await state.clear()
