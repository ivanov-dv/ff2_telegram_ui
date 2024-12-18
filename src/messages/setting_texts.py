SUCCESS_UPDATE_SPACE = (
    '▶️     База изменена на {space_name}\n'
    '▶️     <u>Период:</u> {current_month}_{current_year}'
)
FAIL_UPDATE_SPACE = '❗️ Ошибка при изменении базы. Попробуйте позже ❗️'
CHOOSE_SPACE = (
    '⚙️    <b><u>Выбор базы</u></b>    ⚙️\n'
    '\n'
    'Список доступных баз:\n'
    '\n'
    '⌨️'
)
DELETE_USER = (
    '❗️ Подтвердите удаление аккаунта ❗️\n'
    '❗️ В случае подтверждения все данные будут удалены безвозвратно ❗️'
)
SUCCESS_DELETE_USER = '❗ ️ Аккаунт удален ❗️'
CANCEL_DELETE_USER = '▶️     Вы отменили удаление аккаунта'
NOT_OWNER_SPACE = '❗ Вы не являетесь владельцем текущей базы ❗'
LINKED_CHAT_CONNECTED = (
    '⚙️    <u>Только для своего аккаунта</u>    ⚙️\n'
    '\n'
    '▶️     Чат {linked_chat} подключен.'
)
GET_LINKED_CHAT_ID = (
    '⚙️    <u>Только для своего аккаунта</u>    ⚙️\n'
    '\n'
    '▶️     Введите ID чата, который хотите подключить '
    '(вместе с знаком минус в начале, если он присутствует)'
)
SUCCESS_LINK_CHAT = (
    '▶️     Чат {linked_chat} подключен\n'
    '\n'
    '▶️     <u>База:</u> {current_space}\n'
    '▶️     <u>Период:</u> {current_month}_{current_year}'
)
FAIL_LINK_CHAT = '❗️ Ошибка при подключении чата. Попробуйте позже ❗️'
SUCCESS_DISABLE_LINK_CHAT = (
    '▶️     Чат отключен\n'
    '▶️     <u>База:</u> {current_space}\n'
    '▶️     <u>Период:</u> {current_month}_{current_year}'
)
FAIL_DISABLE_LINK_CHAT = (
    '❗️ Ошибка при отключении чата. Попробуйте позже ❗️'
)
