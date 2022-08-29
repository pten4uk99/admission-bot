from typing import Type

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup

from services import Analyzer


class Handler:
    def __init__(self, states_group: Type[StatesGroup], analyzer: Analyzer):
        self.states_group = states_group
        self.analyzer = analyzer

    async def handler(self, *args, **kwargs):
        """ Обработчик """

        raise NotImplementedError()


class CallbackHandler(Handler):
    async def handler(self, callback: types.CallbackQuery, state: FSMContext):
        raise NotImplementedError()


class MessageHandler(Handler):
    async def handler(self, message: types.Message, state: FSMContext):
        raise NotImplementedError()
