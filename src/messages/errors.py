BASE_ERROR_TEXT = '❗️ {} ❗️'

UNEXPECTED_ERROR = BASE_ERROR_TEXT.format(
    'Непредвиденная ошибка: {error}'
)
CREATE_USER_ERROR = BASE_ERROR_TEXT.format(
    'Ошибка создания пользователя. Попробуйте позже'
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
    'Значение должно быть числом. Например 27 или 5.32'
)
BAСKEND_ERROR = BASE_ERROR_TEXT.format(
    'Сервис временно недоступен. Попробуйте позже'
)
BACKEND_RESPONSE_NOT_EXPECTED = BASE_ERROR_TEXT.format(
    'Неожиданная структура ответа сервера'
)
DELETE_USER_ERROR = BASE_ERROR_TEXT.format(
    'Ошибка удаления пользователя. Попробуйте позже'
)
CREATE_GROUP_ERROR = BASE_ERROR_TEXT.format(
    'Ошибка создания статьи. Попробуйте позже'
)
LIST_GROUP_ERROR = BASE_ERROR_TEXT.format(
    'Ошибка получения списка статей. Попробуйте позже'
)
GET_GROUP_ERROR = BASE_ERROR_TEXT.format(
    'Ошибка получения статьи. Попробуйте позже'
)
DELETE_GROUP_ERROR = BASE_ERROR_TEXT.format(
    'Ошибка удаления статьи. Попробуйте позже'
)
GET_SUMMARY_ERROR = BASE_ERROR_TEXT.format(
    'Ошибка получения отчета за период. Попробуйте позже'
)
ADD_TRANSACTION_ERROR = BASE_ERROR_TEXT.format(
    'Ошибка добавления транзакции. Попробуйте позже'
)
UPDATE_SETTINGS_ERROR = BASE_ERROR_TEXT.format(
    'Ошибка изменения настроек. Попробуйте позже'
)
LINK_USER_ERROR = BASE_ERROR_TEXT.format(
    'Ошибка предоставления доступа пользователю. Попробуйте позже'
)
UNLINK_USER_ERROR = BASE_ERROR_TEXT.format(
    'Ошибка при отвязке пользователя от пространства. Попробуйте позже'
)
