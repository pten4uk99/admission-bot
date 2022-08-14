from architecture.base import Keyboard, CallBackInlineButton

__all__ = [
    'SelectLanguageKeyboard'
]


class RussianLanguageButton(CallBackInlineButton):
    text = 'Русский'


class EnglishLanguageButton(CallBackInlineButton):
    text = 'English'


class JapanLanguageButton(CallBackInlineButton):
    text = '中国人'


class SelectLanguageKeyboard(Keyboard):
    button_classes = [
        RussianLanguageButton,
        EnglishLanguageButton,
        JapanLanguageButton
    ]
