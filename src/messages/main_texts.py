from config import LJUST_DOT_DEFAULT, LJUST_PASS_DEFAULT
from utils.models import Summary

MAIN_TEXT = (
    '<b>'
    '♻️     {first_name}, привет!\n'
    '▶️     <u>Твой ID:</u> {user_id}\n'
    '▶️     <u>База:</u> {space_name}\n'
    '▶️     <u>Период:</u> {current_month}_{current_year}'
    '</b>'
)
CHOOSE_PERIOD = '▶️     Выберите период, в который нужно вносить данные'
SETTINGS = '⚙️    <b><u>Настройки приложения</u></b>    ⚙️'
EMPTY_SUMMARY = (
    '❗️ Пустая таблица ❗️\n'
    '❗️ Внесите данные ❗️'
)
CREATE_GROUP = (
    '▶️     <b><u>Добавление статьи</u></b>\n'
    '\n'
    'Выберите тип статьи\n'
    '\n'
    '⌨️'
)
DELETE_GROUP = (
    '▶️     <b><u>Удаление статьи</u></b>\n'
    '\n'
    'Выберите тип статьи, которую хотите удалить\n'
    '\n'
    '⌨️'
)

ADD_TRANSACTION = (
    '▶️     <b><u>Добавление транзакции</u></b>\n'
    '\n'
    'Выберите тип статьи\n'
    '\n'
    '⌨️'
)


def get_summary_text(summary: Summary) -> str:

    # Начало сообщения
    text = [
        f'▶️     <b><u>База:</u> {summary.summary[0].space.name}\n'
        f'▶️     <u>Период:</u> {summary.summary[0].period_month}_'
        f'{summary.summary[0].period_year}</b>\n\n'
        '<code>'
        f'{'Статья':.<{LJUST_DOT_DEFAULT}} План  / Факт\n'
        '-----------------------------\n'
    ]

    incomes = []
    expenses = []

    for group in summary.summary:
        group_text = (
            f'{group.group_name:.<{LJUST_DOT_DEFAULT}} '
            f'{(round(group.plan_value / 1000, 1)):<{LJUST_PASS_DEFAULT}}/ '
            f'{(round(group.fact_value / 1000, 1)):<{LJUST_PASS_DEFAULT}}\n'
        )
        if group.type_transaction == 'income':
            incomes.append(group_text)
        else:
            expenses.append(group_text)
    if incomes:
        text.extend(incomes)
    else:
        text.append('Доходов нет\n')
    text.append('-----------------------------\n')
    if expenses:
        text.extend(expenses)
    else:
        text.append('Расходов нет\n')
    text.append(
        '-----------------------------\n'
        f'{'Доходы':.<{LJUST_DOT_DEFAULT}} '
        f'{(round(summary.sum_income_plan / 1000, 1)):<{LJUST_PASS_DEFAULT}}/ '
        f'{(round(summary.sum_income_fact / 1000, 1)):<{LJUST_PASS_DEFAULT}}\n'
        f'{'Расходы':.<{LJUST_DOT_DEFAULT}} '
        f'{(round(
            summary.sum_expense_plan / 1000, 1)):<{LJUST_PASS_DEFAULT}}/ '
        f'{(round(
            summary.sum_expense_fact / 1000, 1)):<{LJUST_PASS_DEFAULT}}\n'
        f'{'Сальдо':.<{LJUST_DOT_DEFAULT}} '
        f'{(round(
            summary.balance_plan / 1000, 1)):<{LJUST_PASS_DEFAULT}}/ '
        f'{(round(
            summary.balance_fact / 1000, 1)):<{LJUST_PASS_DEFAULT}}\n'
        f'</code>'
    )
    return ''.join(text)
