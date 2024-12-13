import utils.keyboards as kb
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, KeyboardBuilder
from datetime import date
from typing import Union


class GeneratorKb:
    """Класс для генерации клавиатур."""

    @staticmethod
    def generate_for_choose_period() -> KeyboardBuilder:
        builder = InlineKeyboardBuilder()
        if date.today().month == 1:
            builder.button(text=f"11_{date.today().year-1}",
                           callback_data=f"period_11_{date.today().year-1}")
            builder.button(text=f"12_{date.today().year-1}",
                           callback_data=f"period_12_{date.today().year-1}")
            builder.button(text=f"02_{date.today().year}",
                           callback_data=f"period_02_{date.today().year}")
            builder.button(text=f"03_{date.today().year}",
                           callback_data=f"period_03_{date.today().year}")
            builder.button(text=f"01_{date.today().year}",
                           callback_data=f"period_01_{date.today().year}")
        elif date.today().month == 2:
            builder.button(text=f"12_{date.today().year - 1}",
                           callback_data=f"period_12_{date.today().year - 1}")
            builder.button(text=f"01_{date.today().year}",
                           callback_data=f"period_01_{date.today().year}")
            builder.button(text=f"03_{date.today().year}",
                           callback_data=f"period_03_{date.today().year}")
            builder.button(text=f"04_{date.today().year}",
                           callback_data=f"period_04_{date.today().year}")
            builder.button(text=f"02_{date.today().year}",
                           callback_data=f"period_02_{date.today().year}")
        elif date.today().month == 11:
            builder.button(text=f"09_{date.today().year}",
                           callback_data=f"period_09_{date.today().year}")
            builder.button(text=f"10_{date.today().year}",
                           callback_data=f"period_10_{date.today().year}")
            builder.button(text=f"12_{date.today().year}",
                           callback_data=f"period_12_{date.today().year}")
            builder.button(text=f"01_{date.today().year}",
                           callback_data=f"period_01_{date.today().year+1}")
            builder.button(text=f"11_{date.today().year}",
                           callback_data=f"period_11_{date.today().year}")
        elif date.today().month == 12:
            builder.button(text=f"10_{date.today().year}",
                           callback_data=f"period_10_{date.today().year}")
            builder.button(text=f"11_{date.today().year}",
                           callback_data=f"period_11_{date.today().year}")
            builder.button(text=f"01_{date.today().year+1}",
                           callback_data=f"period_01_{date.today().year+1}")
            builder.button(text=f"02_{date.today().year+1}",
                           callback_data=f"period_02_{date.today().year+1}")
            builder.button(text=f"12_{date.today().year}",
                           callback_data=f"period_12_{date.today().year}")
        else:
            offset_list = [-2, -1, 1, 2]
            for offset in offset_list:
                builder.button(text=f"{str(date.today().month+offset).zfill(2)}_{date.today().year}",
                               callback_data=f"period_{str(date.today().month+offset).zfill(2)}_{date.today().year}")
            builder.button(text=f"{str(date.today().month).zfill(2)}_{date.today().year}",
                           callback_data=f"period_{str(date.today().month).zfill(2)}_{date.today().year}")
        return builder.adjust(2)

    @staticmethod
    def kb_get_list_table(list_table) -> KeyboardBuilder:
        builder = InlineKeyboardBuilder()
        for i in range(len(list_table)):
            builder.button(
                text=f"{list_table[i]}",
                callback_data=f"table_{list_table[i]}"
            )
        return builder.adjust(2)

    @staticmethod
    def generate_choose_base(list_data: Union[tuple, list]) -> InlineKeyboardBuilder:
        builder = InlineKeyboardBuilder()
        for i in range(len(list_data)):
            builder.button(
                text=f"ID {list_data[i][1]}",
                callback_data=f"{list_data[i][0]}"
            )
        return builder

    @staticmethod
    def generate_from_list(list_data: Union[tuple, list]) -> InlineKeyboardBuilder:
        builder = InlineKeyboardBuilder()
        for i in range(len(list_data)):
            builder.button(
                text=f"{list_data[i]}",
                callback_data=f"{list_data[i]}"
            )
        return builder


generator_kb = GeneratorKb()
