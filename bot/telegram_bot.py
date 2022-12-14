from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor

from architecture.achitecture import StateArchitecture
from config import TOKEN
from db import DataBase
from services.analyzer import Analyzer


class TelegramBot:
    token = TOKEN
    connection = DataBase()
    
    def __init__(self):
        self.bot = Bot(token=self.token)
        self.dispatcher = Dispatcher(self.bot, storage=MemoryStorage())
        self.analyzer = Analyzer()
        self.architecture = StateArchitecture(self.bot, self.connection, self.dispatcher, self.analyzer)

    async def on_startup(self, dispatcher):
        self.connection.connect()

        # конечно же, создавать таблицы каждый раз при запуске бота не нужно.
        # Нужно это вынести куда нибудь отдельно
        self.connection.create_tables()
        print('Бот запущен, подключение к базе установлено')
    
    async def on_shutdown(self, dispatcher):
        self.connection.close()
        print('Бот остановлен, подключение с базой разорвано')
    
    def start(self) -> None:
        self.architecture.build()
        
        executor.start_polling(
            self.dispatcher,
            skip_updates=True,
            on_startup=self.on_startup,
            on_shutdown=self.on_shutdown,
        )
        # skip_updates - бот не будет отвечать на сообщения, которые были отправлены, когда он был не онлайн
