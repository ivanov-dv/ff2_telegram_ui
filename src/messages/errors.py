BASE_ERROR_TEXT = '❗️ {} ❗️'

UNEXPECTED_ERROR = BASE_ERROR_TEXT.format(
    'Непредвиденная ошибка: {error}'
)
CREATE_USER_ERROR = BASE_ERROR_TEXT.format(
    'Ошибка создания пользователя'
)
VALIDATE_GROUP_NAME_STR_ERROR = BASE_ERROR_TEXT.format(
    'Название статьи должно быть строкой'
)
VALIDATE_GROUP_NAME_EMPTY_ERROR = BASE_ERROR_TEXT.format(
    'Название статьи не может быть пустым'
)
VALIDATE_GROUP_NAME_TOO_LONG_ERROR = BASE_ERROR_TEXT.format(
    'Название статьи не может быть длиннее {max_len} символов'
)
VALIDATE_DIGIT_VALUE_ERROR = BASE_ERROR_TEXT.format(
    'Значение должно быть числом. Например 27 или 5.32.'
)
