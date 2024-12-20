from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from engine import backend_client, bot
from utils.exceptions import BackendError
from utils import keyboards

router = Router()
router.message.filter(F.chat.type.in_('private'))


@router.callback_query(F.data == 'export_excel')
async def export_excel(callback: types.CallbackQuery, state: FSMContext):
    """Экспорт в Excel."""
    try:
        file_from_buffer = await backend_client.get_export_excel(
            callback.from_user.id
        )
        await bot.send_document(
            callback.from_user.id,
            file_from_buffer
        )
        await bot.send_message(
            callback.from_user.id,
            'Файл отправлен',
            reply_markup=keyboards.FamilyFinanceKb.go_to_main()
        )
        await callback.message.delete()
    except BackendError as e:
        await callback.message.edit_text(
            str(e),
            reply_markup=keyboards.FamilyFinanceKb.go_to_main()
        )
