from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext

from engine import backend_client
from messages import choose_period_texts
from utils.filters import StartWidthFilter
from utils.keyboards import FamilyFinanceKb
from handlers.main_handlers import start_callback

router = Router()
router.message.filter(F.chat.type.in_('private'))


@router.callback_query(StartWidthFilter('period_'))
async def choose_period(callback: types.CallbackQuery, state: FSMContext):
    """Выбор периода."""

    # Очистка состояний.
    await state.clear()

    # Получение текущего состояния пользователя.
    user = await backend_client.get_user(callback.from_user.id)

    # Распаковка нового периода
    *_, new_month_period, new_year_period = callback.data.split('_')

    # Установка нового периода в настройки пользователя.
    user.core_settings.current_month = int(new_month_period)
    user.core_settings.current_year = int(new_year_period)

    # Обновление настроек пользователя в БД.
    new_core_settings = await backend_client.update_core_settings(
        callback.from_user.id,
        user.core_settings
    )

    # Если настройки не были изменены, выдаем сообщение об ошибке.
    if not new_core_settings:
        await callback.message.edit_text(
            choose_period_texts.FAIL_CHOOSE_PERIOD,
            reply_markup=FamilyFinanceKb.go_to_main()
        )
        return

    # Если настройки были изменены, переходим к главному меню.
    await start_callback(callback, state)
