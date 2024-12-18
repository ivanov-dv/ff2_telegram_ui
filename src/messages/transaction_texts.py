from config import MAX_LEN_GROUP_NAME

GET_NAME_FOR_CREATE_GROUP = (
    '▶️     <b><u>Добавление статьи</u></b>\n'
    '\n'
    'Введите название статьи\n'
    f'- <u>не более {MAX_LEN_GROUP_NAME}</u> символов\n'
    '\n'
    '⌨️'
)
GROUP_NAME_IS_EXIST = (
    '❗️     Такая статья уже существует\n'
    '\n'
    'Пожалуйста, введите другое название\n'
    '\n'
    '⌨️'
)
GET_PLAN_VALUE_FOR_CREATE_GROUP = (
    '▶️     <b><u>Добавление статьи</u></b>\n'
    '\n'
    'Статья: {group_name}\n'
    'Введите плановое значение:\n '
    '- в <u>тысячах рублей</u>\n'
    '- в <u>формате числа</u> (например 15 или 2.7)\n'
    '\n'
    '⌨️'
)
SUCCESS_CREATE_GROUP = (
    '▶️  Создана статья {group_name} ({type_value})\n'
    '▶️  Плановое значение: {value} т.р.'
)
FAIL_CREATE_GROUP = '❗️ Ошибка при создании статьи. Попробуйте позже ❗️'
NOTICE_TO_JOINT_CHAT_CREATE_GROUP = (
    '❗️  Пользователь <u>{first_name}</u> ({telegram_id}) добавил статью\n'
    '💾  База: {current_space}\n'
    '💾  Период: {current_month}_{current_year}\n'
    '💾  Статья ({type_value}): {group_name}\n'
    '💾  Плановое значение: {plan_value} т.р.'
)
GROUPS_NOT_EXIST = (
    '❗️ Нет созданных статей ❗️'
)
GET_NAME_FOR_DELETE_GROUP = (
    '▶️     <b><u>Удаление статьи</u></b>\n'
    '\n'
    'Выберите статью, которую хотите удалить\n'
    '\n'
    '⌨️'
)
SUCCESS_DELETE_GROUP = '❗️ Статья {group_name} ({type_value}) удалена ❗️'
NOTICE_TO_JOINT_CHAT_DELETE_GROUP = (
    '❗️  Пользователь <u>{first_name}</u> ({telegram_id}) удалил статью\n'
    '💾  База: {current_space}\n'
    '💾  Период: {current_month}_{current_year}\n'
    '💾  Статья ({type_value}): {group_name}\n'
)
GET_GROUP_ADD_TRANSACTION = (
    '▶️     <b><u>Добавление транзакции</u></b>\n'
    '\n'
    'Выберите статью\n'
    '\n'
    '⌨️'
)
GET_VALUE_ADD_TRANSACTION = (
    '▶️     <b><u>Добавление транзакции</u></b>\n'
    '\n'
    'Статья: <b>{group_name}</b>\n'
    'Введите значение:\n'
    '- в <u>тысячах рублей</u>\n'
    '- в <u>формате числа</u> (например 15 или 2.7)\n'
    '\n'
    '⌨️'
)
GET_DESCRIPTION_ADD_TRANSACTION = (
    '▶️     <b><u>Добавление транзакции</u></b>\n'
    '\n'
    'Введите описание операции\n'
    '\n'
    '⌨️'
)
FAIL_ADD_TRANSACTION = '❗️ Ошибка добавления транзакции. Попробуйте заново. ❗️'
SUCCESS_ADD_TRANSACTION = (
    '♻️  Успешно добавлена транзакция.\n'
    '💾  Период: {current_month}_{current_year}\n'
    '💾  Статья ({type_transaction}): {group_name}\n'
    '💾  Значение: {old_value} т.р. -> {new_value} т.р.\n'
    '💾  Описание: {description}'
)
NOTICE_TO_JOINT_CHAT_ADD_TRANSACTION = (
    '♻️  Пользователь <u>{first_name}</u> ({id_telegram}) добавил запись\n'
    '💾  База: {current_space}\n'
    '💾  Период: {current_month}_{current_year}\n'
    '💾  Статья ({type_transaction}): {group_name}\n'
    '💾  Сумма операции: {value_transaction} т.р.\n'
    '💾  Описание: {description}'
)
