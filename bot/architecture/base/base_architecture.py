from typing import Type, Callable

from aiogram import Bot, Dispatcher, types

from architecture.base.stage import Stage
from db import Connection
from .callback_message_generator import CallbackMessageGenerator
from .stage import StageLink


class BaseArchitecture:
    """ Основное назначение - связывать объекты Stage в определенном порядке """

    stages_classes = None

    def __init__(self, bot: Bot, connection: Connection, dp: Dispatcher):
        self.bot = bot
        self.connection = connection
        self.dp = dp

        assert self.stages_classes is not None
        self.stages = self.init_stages()
        self.link_stages()

    def link_stages(self) -> None:
        """ """

        linker = StageLink(stages=self.stages, message_to_stage_generator=self.get_message_to_stage_generator)
        linker.link_stages()

    def init_stages(self) -> list[Stage]:
        stages = []

        for stage in self.stages_classes:
            stages.append(stage(self.bot, self.dp))

        return stages

    def get_message_to_stage_generator(self, message_text: str = None,
                                       message_markup: types.InlineKeyboardMarkup = None) -> CallbackMessageGenerator:
        return CallbackMessageGenerator(message_text=message_text, message_markup=message_markup)

    def get_first_stage(self) -> Type[Stage]:
        if len(self.stages_classes) > 0:
            return self.stages_classes[0]

    async def unhandled_message(self, message: types.Message):
        await message.answer('Извините, пока что я не умею обрабатывать такие запросы...')

    def build(self):
        for stage in self.stages:
            stage.register()

        # более абстрактные сообщения регистрируем ниже конкретных
        self.dp.register_message_handler(self.unhandled_message)
