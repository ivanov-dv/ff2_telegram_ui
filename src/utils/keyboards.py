"""Создание клавиатур."""

from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from utils.keyboard_generators import GeneratorKb
from utils.models import Summary, Space, UserShort


class FamilyFinanceKb:
    """Базовый класс Inline клавиатуры приложения."""

    default_adjust = 2  # Количество кнопок в строке по умолчанию.

    button_back_to_start = InlineKeyboardButton(
        text='На главную', callback_data='start')
    button_choose_period = InlineKeyboardButton(
        text='Выбрать период', callback_data='choose_period')

    @classmethod
    def go_to_main(cls):
        """Клавиатура для перехода на главную."""
        builder = InlineKeyboardBuilder()
        builder.row(cls.button_back_to_start)
        return builder.as_markup()


class WorkWithBase(FamilyFinanceKb):
    """Класс клавиатуры для работы с базой"""

    button_look = InlineKeyboardButton(
        text='Просмотр', callback_data='look_base')
    button_settings = InlineKeyboardButton(
        text='Настройки', callback_data='settings')
    button_edit = InlineKeyboardButton(
        text='Добавить запись', callback_data='add_transaction')
    button_create_group = InlineKeyboardButton(
        text='Создать статью', callback_data='create_group')
    button_delete_group = InlineKeyboardButton(
        text='Удалить статью', callback_data='delete_group')
    button_income = InlineKeyboardButton(
        text='Доход', callback_data='income')
    button_expense = InlineKeyboardButton(
        text='Расход', callback_data='expense')
    button_general_description = InlineKeyboardButton(
        text='Описание', callback_data='general_description')

    buttons_main_menu = [
        [button_edit, button_look],
        [button_create_group, button_delete_group],
        [FamilyFinanceKb.button_choose_period, button_settings],
        [button_general_description]
    ]
    buttons_choose_type = [
        [button_income, button_expense],
        [FamilyFinanceKb.button_back_to_start]
    ]

    @classmethod
    def main_menu(cls):
        """Клавиатура главного меню."""
        builder = InlineKeyboardBuilder(markup=cls.buttons_main_menu)
        return builder.as_markup()

    @classmethod
    def choose_type(cls):
        """Клавиатура выбора типа операции."""
        builder = InlineKeyboardBuilder(markup=cls.buttons_choose_type)
        return builder.as_markup()

    @classmethod
    def choose_group_name(cls, summary: Summary):
        """Клавиатура выбора статьи."""
        builder = GeneratorKb.generate_choose_group_name(summary)
        builder.row(cls.button_back_to_start)
        builder.adjust(1)
        return builder.as_markup()


class RegistrationKb(FamilyFinanceKb):
    """Класс клавиатуры для регистрации."""

    button_registration = InlineKeyboardButton(
        text='Регистрация', callback_data='registration')
    button_registration_delete_accept = InlineKeyboardButton(
        text='Подтвердить', callback_data='registration_delete_accept')
    button_registration_delete_cancel = InlineKeyboardButton(
        text='Отменить', callback_data='registration_delete_cancel')

    buttons_confirm_delete_registration = [[
        button_registration_delete_accept,
        button_registration_delete_cancel
    ]]

    @classmethod
    def add_registration(cls):
        """Клавиатура для регистрации."""
        builder = InlineKeyboardBuilder()
        builder.row(cls.button_registration)
        return builder.as_markup()

    @classmethod
    def confirm_delete_registration(cls):
        """Клавиатура подтверждения/отмены удаления аккаунта."""
        builder = InlineKeyboardBuilder(
            markup=cls.buttons_confirm_delete_registration
        ).adjust(cls.default_adjust)
        return builder.as_markup()


class SettingsKb(FamilyFinanceKb):
    """Класс клавиатуры для изменения настроек приложения"""

    button_back_to_settings = InlineKeyboardButton(
        text='В настройки', callback_data='settings')
    button_choose_base = InlineKeyboardButton(
        text='Выбрать базу', callback_data='choose_space')
    button_delete_registration = InlineKeyboardButton(
        text='Удалить акк', callback_data='registration_delete')
    button_manage_linked_accounts = InlineKeyboardButton(
        text='Общий доступ', callback_data='linked_accounts')
    button_add_linked_account = InlineKeyboardButton(
        text='Дать доступ', callback_data='linked_accounts_add')
    button_delete_linked_account = InlineKeyboardButton(
        text='Убрать доступ', callback_data='linked_accounts_delete')
    button_instruction_linked_account = InlineKeyboardButton(
        text='Инструкция', callback_data='linked_accounts_instruction')
    button_joint_chat = InlineKeyboardButton(
        text='Подключить чат', callback_data='joint_chat')
    button_joint_chat_delete = InlineKeyboardButton(
        text='Отключить', callback_data='joint_chat_delete')
    button_joint_chat_instruction = InlineKeyboardButton(
        text='Инструкция', callback_data='joint_chat_instruction')

    buttons_back_to_settings = [
        [button_back_to_settings]]
    buttons_settings = [
        [button_choose_base, button_manage_linked_accounts],
        [button_joint_chat, button_delete_registration],
        [FamilyFinanceKb.button_back_to_start]]
    buttons_manage_linked_accounts = [
        [button_add_linked_account],
        [button_delete_linked_account],
        [button_instruction_linked_account],
        [button_back_to_settings]]

    @classmethod
    def back_to_settings(cls):
        """Клавиатура возврата в настройки приложения."""
        builder = InlineKeyboardBuilder(markup=cls.buttons_back_to_settings)
        return builder.as_markup()

    @classmethod
    def settings(cls):
        """Клавиатура меню настроек приложения."""
        builder = InlineKeyboardBuilder(markup=cls.buttons_settings)
        return builder.as_markup()

    @classmethod
    def choose_period(cls):
        """Клавиатура выбора периода."""
        builder = InlineKeyboardBuilder()
        builder.row(cls.button_choose_period)
        return builder.as_markup()

    @classmethod
    def generate_choose_period(cls):
        """Клавиатура генерирующая кнопки периодов для выбора."""
        builder = GeneratorKb.generate_for_choose_period()
        builder.row(cls.button_back_to_start)
        return builder.as_markup()

    @classmethod
    def manage_linked_accounts(cls):
        """Клавиатура меню для управления привязанными аккаунтами."""
        builder = InlineKeyboardBuilder(
            markup=cls.buttons_manage_linked_accounts
        )
        return builder.as_markup()

    @classmethod
    def generate_users_for_unlink(
            cls,
            linked_users: list[UserShort] | tuple[UserShort]
    ):
        """
        Клавиатура генерирует кнопки для выбора пользователя
        и его отвязки от выбранного пространства.
        """
        builder = GeneratorKb.generate_users_for_unlink(linked_users)
        builder.row(cls.button_back_to_settings)
        builder.adjust(1)
        return builder.as_markup()

    @classmethod
    def generate_choose_space(
            cls,
            owner_id,
            spaces: tuple[Space] | list[Space]
    ):
        """
        Клавиатура генерирует кнопки для выбора
        доступного пользователю пространства.
        """
        builder = GeneratorKb.generate_choose_space(owner_id, spaces)
        builder.add(cls.button_back_to_settings)
        builder.adjust(1)
        return builder.as_markup()

    @classmethod
    def joint_chat_add(cls):
        """Клавиатура подключения пользователя к текущему пространству."""
        builder = InlineKeyboardBuilder()
        builder.row(cls.button_joint_chat_instruction)
        builder.row(cls.button_back_to_settings)
        builder.adjust(1)
        return builder.as_markup()

    @classmethod
    def joint_chat_delete(cls):
        """Клавиатура отключения пользователя от текущего пространства."""
        builder = InlineKeyboardBuilder()
        builder.row(cls.button_joint_chat_delete)
        builder.row(cls.button_back_to_settings)
        builder.adjust(1)
        return builder.as_markup()
