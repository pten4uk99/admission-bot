from aiogram import types
from aiogram.dispatcher import FSMContext

from architecture.base import State
from architecture.handlers.base import MessageHandler
from db.models import Student


class StartMessageHandler(MessageHandler):
    async def handler(self, message: types.Message, state: FSMContext = None):
        """ Обработчик, который запускает бота (по команде /start) """

        await message.delete()

        Student.query_.get(chat_id=message.chat.id)
        student = Student.query_.perform_fetch()

        if not student:
            Student.query_.create(chat_id=message.chat.id)
            Student.query_.perform_update()

        state_name = await self.states_group.first()
        state: State = getattr(self.states_group, state_name.split(':')[1])
        await message.answer(text=state.get_text(), reply_markup=state.get_markup())


class UserQuestionHandler(MessageHandler):
    async def handler(self, message: types.Message, state: FSMContext):
        """ Обработка вопросов пользователя после того, как он заполнил все данные о себе """

        self.analyzer.analyze(message.text)
        await message.answer(
            f'Я смог разложить твои слова на вот такие составляющие:\n\n{self.analyzer.data().capitalize()}')


class InStatesMessageHandler(MessageHandler):
    """
    Обработка входящих сообщений от пользователя во время того,
    как он находится в каком то из State
    """

    async def handler(self, message: types.Message, state: FSMContext):
        await message.delete()
