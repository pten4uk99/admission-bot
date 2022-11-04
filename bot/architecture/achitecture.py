from typing import Callable

from aiogram import Bot, Dispatcher

from architecture.handlers.handler_generator import RegisterUserHandlerManager
from architecture.stages.register_user.stages import *
from architecture.stages.state_groups import RegisterUserStateGroup
from db import DataBase
from services import Analyzer


class StateArchitecture:
    """ Основное назначение - связывать объекты Stage в определенном порядке """

    states_group = RegisterUserStateGroup

    def __init__(self, bot: Bot, connection: DataBase, dp: Dispatcher, analyzer: Analyzer):
        self.bot = bot
        self.connection = connection
        self.dp = dp
        self.analyzer = analyzer
        self.handler_generator = self.get_handler_generator()

    def get_handler_generator(self) -> RegisterUserHandlerManager:
        return RegisterUserHandlerManager(
            dp=self.dp,
            states_group=self.states_group,
            analyzer=self.analyzer
        )

    def get_state_handler(self, current_stage: State) -> Callable:
        """ Декоратор, который возвращает обработчик переданного State """

        async def handler(callback: types.CallbackQuery, state: FSMContext):
            await current_stage.handler(callback, state)
            await self.handler_generator.state_callback(callback, state)

        return handler

    def _register_state(self, state: State):
        """ Регистрирует обработчики для переданного State в self.dp """

        self.dp.register_callback_query_handler(self.get_state_handler(state), state=state)
        self.dp.register_message_handler(self.handler_generator.in_state_message, state=state)

    def init_states(self):
        """ Инициализирует все State """

        for state in self.states_group.states:
            state: State
            state.init_keyboard(bot=self.bot, state_group=self.states_group)
            self._register_state(state)

    def build(self):
        self.init_states()
        self.dp.register_message_handler(self.handler_generator.start_message, commands=['start'])
        self.dp.register_message_handler(self.handler_generator.user_question)


if __name__ == '__main__':
    pass
