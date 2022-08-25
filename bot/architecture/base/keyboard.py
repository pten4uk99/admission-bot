from aiogram import Bot
from aiogram.dispatcher.filters.state import StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


class Keyboard:
    """
    Класс клавиатуры. Основное назначение - собирать кнопки.
    
    При наследовании:
    self.row_width - сколько кнопок помещается на строке, по умолчанию - 1
    self.buttons_names - список строк - названий кнопок
    self.add_buttons_to_markup() - в методе прописывается способ добавления кнопок на клавиатуру.
    """

    row_width = 1
    buttons_names: list[str] = None

    def __init__(self, bot: Bot, state_group: StatesGroup):
        self.markup = InlineKeyboardMarkup(row_width=self.row_width)
        self.state_group = state_group

        self.add_buttons_to_markup()

    def get_buttons(self):
        assert self.buttons_names is not None, f'Обязательный атрибут класса {self.__class__.__name__} "button_names"'

        for button_name in self.buttons_names:
            yield InlineKeyboardButton(button_name, callback_data=button_name)

    def add_buttons_to_markup(self) -> None:
        """ Назначает способ добавления кнопок """

        # по умолчанию добавляет кнопки друг под дружку
        for button in self.get_buttons():
            self.markup.add(button)
