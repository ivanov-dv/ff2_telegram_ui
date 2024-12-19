"""Хэндлеры для выбора периода."""

from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext

from engine import backend_client
from utils.exceptions import BackendError
from utils.keyboards import FamilyFinanceKb
from handlers.main_handlers import start_callback

router = Router()
router.message.filter(F.chat.type.in_('private'))


@router.callback_query(F.data.startswith('period_'))
async def choose_period(callback: types.CallbackQuery, state: FSMContext):
    """Выбор периода."""

    # Очистка состояний.
    await state.clear()

    # Распаковка нового периода
    *_, new_month_period, new_year_period = callback.data.split('_')

    try:
        # Обновление настроек пользователя в БД.
        await backend_client.update_core_settings(
            callback.from_user.id,
            {
                'current_month': int(new_month_period),
                'current_year': int(new_year_period)
            }
        )

        # Переходим к главному меню.
        await start_callback(callback, state)

    # Если настройки не были изменены, отправка сообщения об ошибке.
    except BackendError as e:
        await callback.message.edit_text(
            str(e),
            reply_markup=FamilyFinanceKb.go_to_main()
        )
        return
