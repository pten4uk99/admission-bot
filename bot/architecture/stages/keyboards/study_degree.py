from aiogram import types

from architecture.base import CallBackInlineButton, Keyboard

__all__ = [
    'StudyDegreeKeyboard'
]


class BachelorButton(CallBackInlineButton):
    text = 'Бакалавриат/Специалитет'


class MagistracyButton(CallBackInlineButton):
    text = 'Магистратура'


class AspirantButton(CallBackInlineButton):
    text = 'Аспирантура'


class StudyDegreeKeyboard(Keyboard):
    button_classes = [
        BachelorButton,
        MagistracyButton,
        AspirantButton,
    ]
