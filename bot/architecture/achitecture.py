from aiogram import Bot, Dispatcher
from aiogram import types
from aiogram.dispatcher.filters.state import StatesGroup
from aiogram.dispatcher import FSMContext

from architecture.stages.stages import *
from architecture.stages.stages import SelectLanguageState, NationalityState
from db import DataBase
from db.models import Student


class ArchitectureStateGroup(StatesGroup):
    select_language = SelectLanguageState()
    nationality = NationalityState()
    study_degree = StudyDegreeState()
    study_form = StudyFormState()
    select_course = SelectCourseState()
    change_course = ChangeCourseState()


class Architecture:
    """ Основное назначение - связывать объекты Stage в определенном порядке """

    state_group = ArchitectureStateGroup

    def __init__(self, bot: Bot, connection: DataBase, dp: Dispatcher):
        self.bot = bot
        self.connection = connection
        self.dp = dp

    async def handle_start_message(self, message: types.Message):
        await message.delete()

        Student.query_.get(chat_id=message.chat.id)
        student = Student.query_.perform_fetch()

        if not student:
            Student.query_.create(chat_id=message.chat.id)
            Student.query_.perform_update()

        state_name = await self.state_group.first()
        state: State = getattr(self.state_group, state_name.split(':')[1])
        await message.answer(text=state.get_text(), reply_markup=state.get_markup())

    async def _callback_handler(self, callback: types.CallbackQuery, state: FSMContext):
        if callback.data == BACK_BUTTON_NAME or callback.data == 'Поменять направление':
            next_state_name = await self.state_group.previous()
        else:
            next_state_name = await self.state_group.next()

        for state_ in self.state_group.states:
            state_: State
            if state_.state == next_state_name:
                data = await state.get_data()
                text = state_.get_text(data)
                await callback.message.edit_text(text=text, reply_markup=state_.get_markup())
                break

        if callback.data == BACK_BUTTON_NAME or callback.data == 'Поменять направление':
            data = await state.get_data()

            if data.get('current_state', None):
                if self.state_group.states[-1].state == data.get('current_state'):
                    await state.finish()
                    return

            await state.update_data(current_state=next_state_name)

    def get_state_handler(self, current_stage: State):
        async def handler(callback: types.CallbackQuery, state: FSMContext):
            await current_stage.handler(callback, state)
            await self._callback_handler(callback, state)

        return handler

    async def message_handler_in_states(self, message: types.Message, state: FSMContext):
        await message.delete()

    def init_states(self):
        for state in self.state_group.states:
            state: State
            state.init_keyboard(bot=self.bot, state_group=self.state_group)
            self.dp.register_callback_query_handler(self.get_state_handler(state), state=state)
            self.dp.register_message_handler(self.message_handler_in_states, state=state)

    def build(self):
        self.init_states()
        self.dp.register_message_handler(self.handle_start_message, commands=['start'])


if __name__ == '__main__':
    pass
