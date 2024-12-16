from aiogram.utils.keyboard import InlineKeyboardBuilder, KeyboardBuilder
from datetime import date
from typing import Union

from utils.models import Summary


class GeneratorKb:
    """Класс для генерации клавиатур."""

    @staticmethod
    def generate_for_choose_period() -> KeyboardBuilder:
        """
        Генерация кнопок для выбора периода.
        Генерирует кнопку текущего месяца, а также
        кнопки 2 предыдущих и 2 следующих месяцев.
        """
        builder = InlineKeyboardBuilder()
        today = date.today()

        # Если текущий месяц январь.
        if today.month == 1:
            builder.button(
                text=f'11_{today.year - 1}',
                callback_data=f'period_11_{today.year - 1}'
            )
            builder.button(
                text=f'12_{today.year - 1}',
                callback_data=f'period_12_{today.year - 1}'
            )
            builder.button(
                text=f'02_{today.year}',
                callback_data=f'period_02_{today.year}'
            )
            builder.button(
                text=f'03_{today.year}',
                callback_data=f'period_03_{today.year}'
            )
            builder.button(
                text=f'01_{today.year}',
                callback_data=f'period_01_{today.year}'
            )

        # Если текущий месяц февраль.
        elif today.month == 2:
            builder.button(
                text=f'12_{today.year - 1}',
                callback_data=f'period_12_{today.year - 1}'
            )
            builder.button(
                text=f'01_{today.year}',
                callback_data=f'period_01_{today.year}'
            )
            builder.button(
                text=f'03_{today.year}',
                callback_data=f'period_03_{today.year}'
            )
            builder.button(
                text=f'04_{today.year}',
                callback_data=f'period_04_{today.year}'
            )
            builder.button(
                text=f'02_{today.year}',
                callback_data=f'period_02_{today.year}'
            )

        # Если текущий месяц ноябрь.
        elif today.month == 11:
            builder.button(
                text=f'09_{today.year}',
                callback_data=f'period_09_{today.year}'
            )
            builder.button(
                text=f'10_{today.year}',
                callback_data=f'period_10_{today.year}'
            )
            builder.button(
                text=f'12_{today.year}',
                callback_data=f'period_12_{today.year}'
            )
            builder.button(
                text=f'01_{today.year}',
                callback_data=f'period_01_{today.year + 1}'
            )
            builder.button(
                text=f'11_{today.year}',
                callback_data=f'period_11_{today.year}'
            )

        # Если текущий месяц декабрь.
        elif today.month == 12:
            builder.button(
                text=f'10_{today.year}',
                callback_data=f'period_10_{today.year}'
            )
            builder.button(
                text=f'11_{today.year}',
                callback_data=f'period_11_{today.year}'
            )
            builder.button(
                text=f'01_{today.year + 1}',
                callback_data=f'period_01_{today.year + 1}'
            )
            builder.button(
                text=f'02_{today.year + 1}',
                callback_data=f'period_02_{today.year + 1}'
            )
            builder.button(
                text=f'12_{today.year}',
                callback_data=f'period_12_{today.year}'
            )

        # В остальных случаях.
        else:
            offset_list = [-2, -1, 1, 2]
            for offset in offset_list:
                builder.button(
                    text=f'{str(today.month + offset).zfill(2)}_'
                         f'{today.year}',
                    callback_data=f'period_'
                                  f'{str(today.month + offset).zfill(2)}_'
                                  f'{today.year}'
                )
            builder.button(
                text=f'{str(today.month).zfill(2)}_{today.year}',
                callback_data=f'period_{str(today.month).zfill(2)}_'
                              f'{today.year}'
            )
        return builder.adjust(2)

    @staticmethod
    def generate_spaces(spaces: list | tuple) -> KeyboardBuilder:
        builder = InlineKeyboardBuilder()
        for i in range(len(spaces)):
            builder.button(
                text=f'{spaces[i]}',
                callback_data=f'table_{spaces[i]}'
            )
        return builder.adjust(2)

    @staticmethod
    def generate_choose_space(
            list_data: Union[tuple, list]
    ) -> InlineKeyboardBuilder:
        builder = InlineKeyboardBuilder()
        for i in range(len(list_data)):
            builder.button(
                text=f'ID {list_data[i][1]}',
                callback_data=f'{list_data[i][0]}'
            )
        return builder

    @staticmethod
    def generate_choose_group_name(
            summary: Summary
    ) -> InlineKeyboardBuilder:
        builder = InlineKeyboardBuilder()
        for group in summary.summary:
            builder.button(
                text=group.group_name,
                callback_data=f'group_id_{group.id}'
            )
        return builder

    @staticmethod
    def generate_from_list(
            list_data: Union[tuple, list]
    ) -> InlineKeyboardBuilder:
        builder = InlineKeyboardBuilder()
        for i in range(len(list_data)):
            builder.button(
                text=f'{list_data[i]}',
                callback_data=f'{list_data[i]}'
            )
        return builder
