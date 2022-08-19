from typing import Callable

from aiogram import Bot, types

from architecture.base.descriptors import ButtonMessageCallbackDescriptor


class CallBackInlineButton:
    """
    При наследовании:
    
    Принимает message_to_next_stage - функция, которая вызывается в конце обработчика сообщения.
    self._handle_message - может быть переопределен, в нем можно прописать код для обработки сообщения.
    self.handler - при наследовании лучше не трогать, используется для внешнего взаимодействия с классом.
    self.override_callback - если переопределена, то именно она будет срабатывать
    как обработчик сообщения в приоритете.
    
    Использование:
    
    self.callback - должна быть асинхронная функция, вызывается при отправке сообщения.
    self.handler - используется как обработчик сообщений от пользователя.
    """

    text = None
    callback: Callable = ButtonMessageCallbackDescriptor()

    def __init__(self, bot: Bot):
        self.bot = bot

        if self.override_callback.__name__ in self.__class__.__dict__:
            self.callback = self.override_callback

    async def override_callback(self, message: types.Message):
        pass

    async def _handle_message(self, callback: types.CallbackQuery):
        pass

    async def handler(self, callback: types.CallbackQuery) -> None:
        await self._handle_message(callback)
        await self.callback(callback.message)

    def register(self):
        pass


class BackButton(CallBackInlineButton):
    text = 'Назад'

    # async def _handle_message(self, callback: types.CallbackQuery):
    #     await callback.answer('Хватит тыкать, больше ничо нет!')


if __name__ == '__main__':
    print(BackButton.__dict__)
