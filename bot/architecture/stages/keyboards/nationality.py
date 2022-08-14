from architecture.base import Keyboard, CallBackInlineButton

__all__ = [
    'NationalityKeyboard'
]


class YesButton(CallBackInlineButton):
    text = 'Да'


class NoButton(CallBackInlineButton):
    text = 'Нет'


class NationalityKeyboard(Keyboard):
    button_classes = [
        YesButton,
        NoButton
    ]
