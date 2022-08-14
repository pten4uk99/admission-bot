from aiogram import types

from architecture.base import Keyboard, CallBackInlineButton

__all__ = [
    'ChangeCourseKeyboard'
]


class ChangeCourseButton(CallBackInlineButton):
    text = 'Поменять направление'
    
    async def _handle_message(self, callback: types.CallbackQuery):
        await callback.answer('Хватит тыкать, больше ничо нет!')


class ChangeCourseKeyboard(Keyboard):
    button_classes = [
        ChangeCourseButton
    ]
