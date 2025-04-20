"""Генерация кнопок для клавиатуры."""

from aiogram.utils.keyboard import InlineKeyboardBuilder, KeyboardBuilder
from datetime import date

from utils.models import Summary, Space, UserShort


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
                text=f'01_{today.year}',
                callback_data=f'period_01_{today.year}'
            )
            builder.button(
                text=f'02_{today.year}',
                callback_data=f'period_02_{today.year}'
            )
            builder.button(
                text=f'03_{today.year}',
                callback_data=f'period_03_{today.year}'
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
                text=f'02_{today.year}',
                callback_data=f'period_02_{today.year}'
            )
            builder.button(
                text=f'03_{today.year}',
                callback_data=f'period_03_{today.year}'
            )
            builder.button(
                text=f'04_{today.year}',
                callback_data=f'period_04_{today.year}'
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
                text=f'11_{today.year}',
                callback_data=f'period_11_{today.year}'
            )
            builder.button(
                text=f'12_{today.year}',
                callback_data=f'period_12_{today.year}'
            )
            builder.button(
                text=f'01_{today.year}',
                callback_data=f'period_01_{today.year + 1}'
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
                text=f'12_{today.year}',
                callback_data=f'period_12_{today.year}'
            )
            builder.button(
                text=f'01_{today.year + 1}',
                callback_data=f'period_01_{today.year + 1}'
            )
            builder.button(
                text=f'02_{today.year + 1}',
                callback_data=f'period_02_{today.year + 1}'
            )

        # В остальных случаях.
        else:
            for offset in range(-2, 3):
                builder.button(
                    text=f'{str(today.month + offset).zfill(2)}_'
                         f'{today.year}',
                    callback_data=f'period_'
                                  f'{str(today.month + offset).zfill(2)}_'
                                  f'{today.year}'
                )
        return builder.adjust(2, 1, 2)

    @staticmethod
    def generate_choose_space(
            owner_id: int,
            spaces: tuple[Space] | list[Space]
    ) -> InlineKeyboardBuilder:
        """Генерация кнопок для выбора пространства."""
        builder = InlineKeyboardBuilder()
        for space in spaces:
            owner = space.owner_username
            if int(space.owner_id) == int(owner_id):
                owner = 'Моя'  # Если пространство принадлежит пользователю.
            builder.button(
                text=f'{space.name} ({owner})',
                callback_data=f'choose_space_{space.id}'
            )
        return builder

    @staticmethod
    def generate_choose_group_name(
            summary: Summary
    ) -> InlineKeyboardBuilder:
        """Генерация кнопок для выбора названия статьи."""
        builder = InlineKeyboardBuilder()
        for group in summary.summary:
            builder.button(
                text=group.group_name,
                callback_data=f'group_id_{group.id}'
            )
        return builder

    @staticmethod
    def generate_users_for_unlink(
            linked_users: list[UserShort] | tuple[UserShort]
    ) -> InlineKeyboardBuilder:
        """
        Генерация кнопок пользователей (подключенных)
        для их отключения от пространства.
        """
        builder = InlineKeyboardBuilder()
        for user in linked_users:
            builder.button(
                text=f'{user.username}',
                callback_data=f'{user.id}'
            )
        return builder


    @staticmethod
    def generate_years(years: list[str]) -> KeyboardBuilder:
        """
        Генерация кнопок годов.
        """
        builder = InlineKeyboardBuilder()
        for year in years:
            builder.button(
                text=f'{year}',
                callback_data=f'all_periods_year_{year}'
            )
        return builder.adjust(2)

    @classmethod
    def generate_months(cls, months: list[str]) -> KeyboardBuilder:
        """
        Генерация кнопок месяцев.
        """
        builder = InlineKeyboardBuilder()
        for month in months:
            builder.button(
                text=f'{month}',
                callback_data=f'all_periods_month_{month}'
            )
        return builder.adjust(len(months) // 2)
