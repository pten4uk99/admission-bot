from typing import Type, Callable

from aiogram import Bot, Dispatcher, types

from .descriptors import MessageCallbackDescriptor
from .keyboard import Keyboard
from architecture.utils import get_callback_data_name


class Stage:
    """
    При наследовании:
    
    self.register_message_handlers() - можно переопределять, в нем регистрируются обработчкии сообщений
    self.register_keyboard_handlers() - можно переопределять, в нем регистрируются обработчики нажатий на кнопки
    
    Использование:
    
    self.to_next_stage() - функция-обработчик, которая будет вызываться при переходе на следующий этап
    self.to_previous_stage() - функция-обработчик, которая будет вызываться при переходе на предыдущий этап
    self.register() - регистрирует обработчики сообщений
    
    Последовательность действий:
    
    """
    
    text = None
    keyboard_class: Type[Keyboard] = None
    
    to_next_stage: Callable = MessageCallbackDescriptor()
    to_previous_stage: Callable = MessageCallbackDescriptor()
    
    def __init__(self, bot: Bot, dp: Dispatcher):
        self.bot = bot
        self.dp = dp
        self.keyboard = None
        self.init_keyboard()

    def init_keyboard(self):
        if self.keyboard_class is not None:
            self.keyboard = self.keyboard_class(self.bot)
    
    def register_message_handlers(self):
        """ В этом методе прописывается регистрация обработчиков message_handler """
        
        pass
    
    def register_keyboard_handlers(self):
        """ Регистрирует callback_query_handler для всех кнопок в self.keyboard """
        
        keyboard = getattr(self, 'keyboard', None)
        
        if keyboard is not None:
            for button in self.keyboard.button_class_objects:
                self.dp.register_callback_query_handler(button.handler, text=get_callback_data_name(button))
    
    def _register_keyboard(self):
        if self.keyboard is not None:
            self.keyboard.to_next_stage = self.to_next_stage
            self.keyboard.to_previous_stage = self.to_previous_stage
            self.keyboard.register()
    
    def _register_handlers(self):
        self.register_message_handlers()
        self.register_keyboard_handlers()
    
    def register(self):
        """ Интерфейсный метод. Регистрирует все обработчики объекта """
        
        self._register_keyboard()
        self._register_handlers()


class MessageHandlerStage(Stage):
    """ Этап, который может обрабатывать сообщения """
    
    async def _handle_message(self, message: types.Message):
        pass
    
    async def _handler(self, message: types.Message):
        await self._handle_message(message)
        await self.to_next_stage(message)
