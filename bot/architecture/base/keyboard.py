from typing import Type, Callable

from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from architecture.base.descriptors import MessageCallbackDescriptor
from architecture.base.button import CallBackInlineButton, BackButton
from architecture.utils import get_callback_data_name


class Keyboard:
    """
    Класс клавиатуры. Основное назначение - собирать кнопки.
    
    При наследовании:
    
    self.button_classes - список кнопок
    self.add_buttons_to_markup() - в методе прописывается способ добавления кнопок на клавиатуру.
    """

    row_width = 1
    button_classes: list[Type[CallBackInlineButton]] = []
    add_back_button: bool = True

    to_next_stage: Callable = MessageCallbackDescriptor()
    to_previous_stage: Callable = MessageCallbackDescriptor()

    def __init__(self, bot: Bot):
        self.markup = InlineKeyboardMarkup(row_width=self.row_width)

        self.back_button: CallBackInlineButton = None
        self.button_class_objects = self.get_button_class_objects(bot)
        self.buttons = self.init_buttons()
        self.add_buttons_to_markup()

    def get_button_class_objects(self, bot: Bot) -> list[CallBackInlineButton]:
        buttons = []

        for button_class in self.button_classes:
            buttons.append(button_class(bot))

        if self.add_back_button:
            self.back_button = self._get_back_button_class()(bot)
            buttons.append(self.back_button)

        return buttons

    def init_buttons(self) -> list[InlineKeyboardButton]:
        buttons = []

        for button in self.button_class_objects:
            buttons.append(InlineKeyboardButton(button.text, callback_data=get_callback_data_name(button)))

        return buttons

    @staticmethod
    def _get_back_button_class() -> Type[CallBackInlineButton]:
        """ Можно переопределять. Возвращает класс, используемый для кнопки "Назад" """

        return BackButton

    def _bind_back_button_callback(self):
        """ Добавляет к кнопке callback """

        if self.back_button is not None:

            self.back_button.callback = self.to_previous_stage

    def add_buttons_to_markup(self) -> None:
        """ Назначает способ добавления кнопок """

        # по умолчанию добавляет кнопки друг под дружку
        for button in self.buttons:
            self.markup.add(button)

    def register(self):
        for button in self.button_class_objects:
            button.callback = self.to_next_stage

        self._bind_back_button_callback()
