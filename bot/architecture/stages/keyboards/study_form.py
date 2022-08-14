from aiogram import types

from architecture.base import CallBackInlineButton, Keyboard

__all__ = [
    'StudyFormKeyboard'
]


class FullTime(CallBackInlineButton):
    text = 'Очная'


class HalfTime(CallBackInlineButton):
    text = 'Очно-заочная'


class Correspondence(CallBackInlineButton):
    text = 'Заочная'


class StudyFormKeyboard(Keyboard):
    button_classes = [
        FullTime,
        HalfTime,
        Correspondence
    ]
