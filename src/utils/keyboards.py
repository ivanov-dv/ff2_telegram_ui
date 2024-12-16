from aiogram.types import InlineKeyboardButton
from aiogram.types.login_url import LoginUrl
from aiogram.utils.keyboard import InlineKeyboardBuilder

from utils.keyboard_generators import GeneratorKb


class BaseKb:
    """Базовый класс, который определяет кол-во кнопок в строке"""
    default_adjust = 2


class FamilyFinanceKb(BaseKb):
    """Класс Inline клавиатуры приложения"""

    button_back_to_start = InlineKeyboardButton(
        text='На главную', callback_data='start')
    button_choose_period = InlineKeyboardButton(
        text='Выбрать период', callback_data='choose_period')

    @classmethod
    def go_to_main(cls):
        """Стартовая клавиатура."""
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
        [FamilyFinanceKb.button_back_to_start]]

    @classmethod
    def main(cls):
        builder = InlineKeyboardBuilder(markup=cls.buttons_main_menu)
        return builder.as_markup()

    @classmethod
    def choose_type(cls):
        builder = InlineKeyboardBuilder(markup=cls.buttons_choose_type)
        return builder.as_markup()

    @classmethod
    def choose_group_name(cls, data_list):
        builder = GeneratorKb.generate_from_list(data_list)
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
        builder = InlineKeyboardBuilder()
        builder.row(cls.button_registration)
        return builder.as_markup()

    @classmethod
    def confirm_delete_registration(cls):
        builder = InlineKeyboardBuilder(
            markup=cls.buttons_confirm_delete_registration
        ).adjust(cls.default_adjust)
        return builder.as_markup()


class SettingsKb(FamilyFinanceKb):
    """Класс клавиатуры для изменения настроек приложения"""

    button_back_to_settings = InlineKeyboardButton(
        text='В настройки', callback_data='settings')
    button_choose_base = InlineKeyboardButton(
        text='Выбрать базу', callback_data='choose_base')
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
        builder = InlineKeyboardBuilder(markup=cls.buttons_back_to_settings)
        return builder.as_markup()

    @classmethod
    def settings(cls):
        builder = InlineKeyboardBuilder(markup=cls.buttons_settings)
        return builder.as_markup()

    @classmethod
    def choose_period(cls):
        builder = InlineKeyboardBuilder()
        builder.row(cls.button_choose_period)
        return builder.as_markup()

    @classmethod
    def choose_period_list(cls):
        builder = GeneratorKb.generate_for_choose_period()
        builder.row(cls.button_back_to_start)
        return builder.as_markup()

    @classmethod
    def manage_linked_accounts(cls):
        builder = InlineKeyboardBuilder(
            markup=cls.buttons_manage_linked_accounts
        )
        return builder.as_markup()

    @classmethod
    def generate_kb_from_list(cls, data_list):
        builder = GeneratorKb.generate_from_list(data_list)
        builder.row(cls.button_back_to_settings)
        builder.adjust(1)
        return builder.as_markup()

    @classmethod
    def generate_choose_space(cls, id_telegram, data_list):
        button = InlineKeyboardButton(
            text='Моя база',
            callback_data=f'{id_telegram}'
        )
        builder = GeneratorKb.generate_choose_space(data_list)
        builder.add(button)
        builder.add(cls.button_back_to_settings)
        builder.adjust(1)
        return builder.as_markup()

    @classmethod
    def joint_chat_add(cls):
        builder = InlineKeyboardBuilder()
        builder.row(cls.button_joint_chat_instruction)
        builder.row(cls.button_back_to_settings)
        builder.adjust(1)
        return builder.as_markup()

    @classmethod
    def joint_chat_delete(cls):
        builder = InlineKeyboardBuilder()
        builder.row(cls.button_joint_chat_delete)
        builder.row(cls.button_back_to_settings)
        builder.adjust(1)
        return builder.as_markup()