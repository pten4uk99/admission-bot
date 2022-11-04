from aiogram import types
from aiogram.dispatcher import FSMContext

from architecture.base import State
from architecture.stages.subscription_send.keyboards import StudyDegreeKeyboard, StudyFormKeyboard, SelectCourseKeyboard
from config import BACK_BUTTON_NAME


class StudyDegreeSendState(State):
    """ Состояние выбора степени обучения """

    text = 'Ю нид ту селект несессари тэгс фор сенд ту юзерс.' \
           'Выберите степень обучения:'
    keyboard_class = StudyDegreeKeyboard

    async def handler(self, callback: types.CallbackQuery, state: FSMContext):
        if callback.data != BACK_BUTTON_NAME:
            await state.update_data(study_degree=callback.data)
            await callback.answer('Выбранная степень обучения сохранена')


class StudyFormSendState(State):
    """ Этап выбора формы обучения """

    text = 'Выберите форму обучения'
    keyboard_class = StudyFormKeyboard

    async def handler(self, callback: types.CallbackQuery, state: FSMContext):
        if callback.data != BACK_BUTTON_NAME:
            await state.update_data(study_form=callback.data)
            await callback.answer('Выбранная форма обучения сохранена')


class SelectCourseSendState(State):
    """ Этап выбора направления """

    text = 'Выберите ваше направление'
    keyboard_class = SelectCourseKeyboard

    async def handler(self, callback: types.CallbackQuery, state: FSMContext):
        if callback.data != BACK_BUTTON_NAME:
            await state.update_data(study_form=callback.data)
            await callback.answer('Выбранное направление сохранено')


class FinishSendState(State):
    """ Этап выбора направления """

    text = 'Сообщение успешно отправлено'

    async def handler(self, callback: types.CallbackQuery, state: FSMContext):
        if callback.data != BACK_BUTTON_NAME:
            await state.get_state()
            await callback.answer('Передаем')
