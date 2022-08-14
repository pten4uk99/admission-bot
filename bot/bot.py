from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor

from architecture.achitecture import Architecture
from config import TOKEN
from db import Connection


class TelegramBot:
    token = TOKEN
    connection = Connection()
    
    def __init__(self):
        self.bot = Bot(token=self.token)
        self.dispatcher = Dispatcher(self.bot, storage=MemoryStorage())
        self.architecture = Architecture(self.bot, self.connection, self.dispatcher)
    
    async def on_startup(self, dispatcher):
        self.connection.connect()
        print('Бот запущен')
    
    async def on_shutdown(self, dispatcher):
        self.connection.close()
        print('Бот остановлен')
    
    def start(self) -> None:
        self.architecture.build()
        
        executor.start_polling(
            self.dispatcher,
            skip_updates=True,
            on_startup=self.on_startup,
            on_shutdown=self.on_shutdown,
        )
        # skip_updates - бот не будет отвечать на сообщения, которые были отправлены, когда он был не онлайн
