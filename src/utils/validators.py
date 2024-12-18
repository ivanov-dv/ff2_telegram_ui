from config import MAX_LEN_GROUP_NAME


def validate_group_name(group_name: str) -> tuple[str | bool, str]:
    if not isinstance(group_name, str):
        return False, 'Название статьи должно быть строкой'
    strip_group_name = group_name.strip()
    if not strip_group_name:
        return False, 'Название статьи не может быть пустым'
    if len(strip_group_name) > MAX_LEN_GROUP_NAME:
        return (
            False,
            'Название статьи не может быть '
            f'длиннее {MAX_LEN_GROUP_NAME} символов'
        )
    return strip_group_name, ''


def validate_digit_value(value):
    try:
        return round(float(value) * 1000, 2), ''
    except ValueError:
        return False, 'Значение должно быть числом. Например 27 или 5.32.'
