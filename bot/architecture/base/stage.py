from typing import Type

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State as BaseState

from .keyboard import Keyboard


class State(BaseState):
    """
    При наследовании:
     self.text - текст сообщения
     self.keyboard_class: Keyboard - класс клавиатуры

     self.handler() - обработчик для текущего стейта, для каждого можно задать уникальный
    """

    text: str = None
    keyboard_class: Type[Keyboard] = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.keyboard = None

    def get_text(self, *args, **kwargs) -> str:
        return self.text or ''

    def init_keyboard(self, *args, **kwargs):
        assert self.keyboard_class is not None, 'Не передан атрибут "keyboard_class"'
        self.keyboard = self.keyboard_class(*args, **kwargs)

    def get_markup(self):
        assert self.keyboard is not None, 'Метод "init_keyboard" не был вызван'
        return self.keyboard.markup

    async def handler(self, callback: types.CallbackQuery, state: FSMContext):
        """
        Тут можно прописать необходимые действия,
        которые будут срабатывать каждый раз на текущем State.
        """

        pass
