from typing import Type, Callable

from aiogram import Dispatcher
from aiogram.dispatcher.filters.state import StatesGroup

from architecture.handlers.base import Handler
from architecture.handlers.callback_handlers import StateCallbackHandler
from architecture.handlers.message_handlers import StartMessageHandler, UserQuestionHandler, InStatesMessageHandler
from services import Analyzer


class HandlerDescriptor:
    def __set_name__(self, owner, name):
        assert issubclass(owner, HandlerManager), (
            f'Дескриптор {self.__class__} может быть установлен только для {HandlerManager} класса'
        )
        self.instance = owner
        self.name = name

    def __get__(self, instance, owner):
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        instance.__dict__[self.name] = self._get_handler(instance, value)

    def _get_handler_method(self, handler: Handler) -> Callable:
        """ Возвращает основной интерфейсный метод обработчика """

        return handler.handler

    def _init_handler(self, instance, handler: Type[Handler]) -> Handler:
        """ Инициализирует обработчик """

        return handler(analyzer=instance.analyzer, states_group=instance.states_group)

    def _get_handler(self, instance, handler_class: Type[Handler]) -> Callable:
        """ Возвращает интерфейсный метод проинициализированного обработчика """

        handler = self._init_handler(instance, handler_class)
        return self._get_handler_method(handler)


class HandlerManager:
    def __init__(self, dp: Dispatcher, states_group: Type[StatesGroup], analyzer: Analyzer):
        self.dp = dp
        self.states_group = states_group
        self.analyzer = analyzer

        self.init_handlers()

    def init_handlers(self):
        """ Инициализирует обработчики """

        raise NotImplementedError()


class RegisterUserHandlerManager(HandlerManager):
    state_callback = HandlerDescriptor()
    start_message = HandlerDescriptor()
    user_question = HandlerDescriptor()
    in_state_message = HandlerDescriptor()

    def init_handlers(self):
        self.state_callback = StateCallbackHandler
        self.start_message = StartMessageHandler
        self.user_question = UserQuestionHandler
        self.in_state_message = InStatesMessageHandler
