from typing import Type, Callable

from aiogram import Bot, Dispatcher, types

from .stage import Stage
from db import Connection


class BaseArchitecture:
    """ Основное назначение - связывать объекты Stage в определенном порядке """
    
    stages_classes = None
    
    def __init__(self, bot: Bot, connection: Connection, dp: Dispatcher):
        self.bot = bot
        self.connection = connection
        self.dp = dp
        
        assert self.stages_classes is not None
        self.stages = self.init_stages()
    
    def get_stage(self, stage_class: Type[Stage]) -> Stage:
        """ Инициализирует переданный объект Stage """
        
        return stage_class(self.bot, self.dp)
    
    def link_stages(self, last_stage: Stage, current_stage: Stage = None) -> Stage:
        """
        Если передан current_stage, то делает ссылку в last_stage на current_stage.
        Возвращает last_stage
        """
        
        if current_stage is not None:
            last_stage.to_next_stage = self.get_message_to_stage(
                current_stage.text, getattr(current_stage.keyboard, 'markup', None))
            current_stage.to_previous_stage = self.get_message_to_stage(
                last_stage.text, getattr(last_stage.keyboard, 'markup', None))
        
        return last_stage
    
    def init_stages(self) -> list[Stage]:
        stages = []
        
        last_stage_index = 0
        current_stage_index = 1
        
        # проходимся в цикле по всем этапам по очереди
        while current_stage_index < len(self.stages_classes) + 1:
            # предыдущий этап
            last_stage_class = self.stages_classes[last_stage_index]
            last_stage = self.get_stage(last_stage_class)
            
            # если дошли до конца списка, то добавляем в конец last_stage
            if current_stage_index == len(self.stages_classes):
                stage_obj = self.link_stages(last_stage)
            # иначе меняем current_stage на следующий по списку
            else:
                current_stage_class = self.stages_classes[current_stage_index]
                current_stage = self.get_stage(current_stage_class)
                stage_obj = self.link_stages(last_stage, current_stage)
            
            stages.append(stage_obj)
            
            last_stage_index += 1
            current_stage_index += 1
        
        return stages
    
    def get_message_to_stage(self, message_text: str = None,
                             message_markup: types.InlineKeyboardMarkup = None) -> Callable:
        raise NotImplementedError()
    
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


