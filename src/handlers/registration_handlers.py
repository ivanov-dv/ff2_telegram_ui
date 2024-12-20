"""Хэндлеры для регистрации."""

from aiogram import Router, F, types

from messages import setting_texts
from engine import backend_client
from utils import keyboards
from utils.exceptions import BackendError

router = Router()
router.message.filter(F.chat.type.in_('private'))


@router.callback_query(F.data == 'registration_delete')
async def registration_delete(callback: types.CallbackQuery):
    """Предупреждающее сообщение перед удалением аккаунта."""
    await callback.message.edit_text(
        setting_texts.DELETE_USER,
        reply_markup=keyboards.RegistrationKb.confirm_delete_registration()
    )


@router.callback_query(F.data == 'registration_delete_accept')
async def registration_delete_accept(callback: types.CallbackQuery):
    """Удаление аккаунта."""
    try:
        # Запрос на удаление пользователя.
        await backend_client.delete_user(callback.from_user.id)

        # Сообщение об успешном удалении.
        await callback.message.edit_text(
            setting_texts.SUCCESS_DELETE_USER,
            reply_markup=keyboards.FamilyFinanceKb.go_to_main()
        )

    # Если произошла ошибка, отправка сообщения о ней.
    except BackendError as e:
        await callback.message.edit_text(
            str(e),
            reply_markup=keyboards.FamilyFinanceKb.go_to_main()
        )


@router.callback_query(F.data == 'registration_delete_cancel')
async def registration_delete_cancel(callback: types.CallbackQuery):
    """Отмена удаления аккаунта."""
    await callback.message.edit_text(
        setting_texts.CANCEL_DELETE_USER,
        reply_markup=keyboards.FamilyFinanceKb.go_to_main()
    )
