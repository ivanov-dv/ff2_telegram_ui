"""Валидаторы входящих данных от пользователя."""

import logging

from config import MAX_LEN_GROUP_NAME
from messages import errors

logger = logging.getLogger(__name__)


def validate_group_name(group_name: str) -> tuple[str | bool, str]:
    """Валидация названия статьи."""

    # Проверка, что входные данные являются строкой.
    if not isinstance(group_name, str):
        logger.debug(f'{errors.VALIDATE_GROUP_NAME_STR_ERROR} {group_name=}')
        return False, errors.VALIDATE_GROUP_NAME_STR_ERROR

    # Удаление пробелов.
    strip_group_name = group_name.strip()

    # Проверка, что название статьи не пустое.
    if not strip_group_name:
        logger.debug(f'{errors.VALIDATE_GROUP_NAME_EMPTY_ERROR} {group_name=}')
        return False, errors.VALIDATE_GROUP_NAME_EMPTY_ERROR

    # Проверка, что название статьи не длиннее максимальной длины.
    if len(strip_group_name) > MAX_LEN_GROUP_NAME:
        logger.debug(
            f'{errors.VALIDATE_GROUP_NAME_TOO_LONG_ERROR} {group_name=}'
        )
        return (
            False,
            errors.VALIDATE_GROUP_NAME_TOO_LONG_ERROR.format(
                max_len=MAX_LEN_GROUP_NAME
            )
        )
    return strip_group_name, ''


def validate_digit_value(value):
    """Валидация ввода числового значения и преобразование тысяч в число."""
    try:
        return round(float(value) * 1000, 2), ''
    except ValueError:
        logger.debug(f'{errors.VALIDATE_DIGIT_VALUE_ERROR} {value=}')
        return False, errors.VALIDATE_DIGIT_VALUE_ERROR
