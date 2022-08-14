from typing import Type, Callable

from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from architecture.base.descriptors import MessageCallbackDescriptor
from architecture.base.button import CallBackInlineButton
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
    
    to_next_stage: Callable = MessageCallbackDescriptor()
    to_previous_stage: Callable = MessageCallbackDescriptor()
    
    def __init__(self, bot: Bot):
        self.initialized = False
        self.markup = InlineKeyboardMarkup(row_width=self.row_width)
        self.button_class_objects = self.get_button_class_objects(bot)
        self.buttons = self.init_buttons()
        self.add_buttons_to_markup()

    def get_button_class_objects(self, bot: Bot) -> list[CallBackInlineButton]:
        buttons = []
        
        for button_class in self.button_classes:
            buttons.append(button_class(bot))
        
        return buttons
    
    def init_buttons(self) -> list[InlineKeyboardButton]:
        buttons = []
        
        for button in self.button_class_objects:
            buttons.append(InlineKeyboardButton(button.text, callback_data=get_callback_data_name(button)))
            
        self.initialized = True
        return buttons
    
    def add_buttons_to_markup(self) -> None:
        """ Назначает способ добавления кнопок """
        
        # по умолчанию добавляет кнопки друг под дружку
        for button in self.buttons:
            self.markup.add(button)
    
    def register(self):
        for button in self.button_class_objects:
            button.callback = self.to_next_stage
