"""FSM состояния приложения."""

from aiogram.fsm.state import State, StatesGroup


class AdminState(StatesGroup):
    reboot = State()


class CreateGroupState(StatesGroup):
    get_type = State()
    get_name = State()
    get_plan_value = State()


class DeleteGroupState(StatesGroup):
    get_type = State()
    get_name = State()


class AddTransaction(StatesGroup):
    get_type = State()
    get_group = State()
    get_value = State()
    get_description = State()


class LinkedAccounts(StatesGroup):
    get_id_linked_account_for_add = State()
    get_id_linked_account_for_delete = State()


class ChooseBase(StatesGroup):
    get_id_base = State()


class JointChat(StatesGroup):
    get_id_joint_chat = State()


class ChooseArchive(StatesGroup):
    get_year = State()
    get_month = State()
