from aiogram import types
from aiogram.dispatcher import FSMContext

from architecture.base import State
from architecture.handlers.base import MessageHandler
from data.questions import KEYWORDS, COMPARISONS
from db.models import Student, Comparison, Keyword
from services import AnalysisManager


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


class InStatesMessageHandler(MessageHandler):
    """
    Обработка входящих сообщений от пользователя во время того,
    как он находится в каком то из State
    """

    async def handler(self, message: types.Message, state: FSMContext):
        await message.delete()


class UserQuestionHandler(MessageHandler):
    async def __init_questions(self):
        for index, comparison in enumerate(COMPARISONS):
            Comparison.query_.create(pk=index + 1, answer=comparison)
            Comparison.query_.perform_update()

        for index, keywords_tuple in enumerate(KEYWORDS):
            for keyword in keywords_tuple:
                Keyword.query_.create(comparison=index + 1, source=keyword)
                Keyword.query_.perform_update()

    async def handler(self, message: types.Message, state: FSMContext):
        """ Обработка вопросов пользователя после того, как он заполнил все данные о себе """

        if message.text == '/init_questions':
            await self.__init_questions()
            return await message.answer(f'<b>Все прошло успешно!</b>', parse_mode=types.ParseMode.HTML)

        manager = AnalysisManager(message.text)
        answer_list = manager.answer()
        joined_answers = "\n\n".join(answer_list)
        if len(answer_list) > 1:
            await message.answer(
                'Я не совсем точно смог распознать твой вопрос, возможно тебе подойдут эти ответы:'
                f'\n\n{joined_answers}', parse_mode=types.ParseMode.HTML)
        elif len(answer_list) == 1:
            await message.answer(answer_list[0], parse_mode=types.ParseMode.HTML)
        else:
            await message.answer('К сожалению, я не совсем понимаю, что ты имеешь ввиду')


class SubscriptionSendHandler(MessageHandler):
    async def handler(self, message: types.Message, state: FSMContext):

        await message.answer('Ты жопошник)')

