from aiogram import types
from aiogram.dispatcher import FSMContext
from architecture.base.stage import State
from db.models import Student
from .keyboards import *


class SelectLanguageState(State):
    text = "Выберите язык/Select Language"
    keyboard_class = SelectLanguageKeyboard

    async def handler(self, callback: types.CallbackQuery, state: FSMContext):
        if callback.data != BACK_BUTTON_NAME and callback.data != 'Поменять направление':
            Student.query_.get(chat_id=callback.message.chat.id)
            student: Student = Student.query_.perform_fetch()

            student.language = callback.data
            student.save()
            await callback.answer('Выбранный язык сохранен')


class NationalityState(State):
    text = "Гражданство РФ?"
    keyboard_class = NationalityKeyboard

    async def handler(self, callback: types.CallbackQuery, state: FSMContext):
        if callback.data != BACK_BUTTON_NAME and callback.data != 'Поменять направление':
            Student.query_.get(chat_id=callback.message.chat.id)
            student: Student = Student.query_.perform_fetch()

            student.russian_nationality = callback.data
            student.save()

            await callback.answer('Ваш ответ сохранен')


class StudyDegreeState(State):
    """ Состояние выбора степени обучения """

    text = 'Привет! Я бот-помощник {}. ' \
           'У меня ты можешь узнать любой ответ на вопрос о поступлении. ' \
           'Я буду уведомлять о важных событиях на протяжении всего процесса поступления. ' \
           'Не отписывайтесь от меня! Выберите степень обучения.'
    keyboard_class = StudyDegreeKeyboard

    async def handler(self, callback: types.CallbackQuery, state: FSMContext):
        if callback.data != BACK_BUTTON_NAME and callback.data != 'Поменять направление':
            Student.query_.get(chat_id=callback.message.chat.id)
            student: Student = Student.query_.perform_fetch()

            student.study_degree = callback.data
            student.save()
            await callback.answer('Выбранная степень обучения сохранена')


class StudyFormState(State):
    """ Этап выбора формы обучения """

    text = 'Выберите форму обучения'
    keyboard_class = StudyFormKeyboard

    async def handler(self, callback: types.CallbackQuery, state: FSMContext):
        if callback.data != BACK_BUTTON_NAME and callback.data != 'Поменять направление':
            Student.query_.get(chat_id=callback.message.chat.id)
            student: Student = Student.query_.perform_fetch()

            student.study_form = callback.data
            student.save()
            await callback.answer('Выбранная форма обучения сохранена')


class SelectCourseState(State):
    """ Этап выбора направления """

    text = 'Выберите ваше направление'
    keyboard_class = SelectCourseKeyboard

    async def handler(self, callback: types.CallbackQuery, state: FSMContext):
        if callback.data != BACK_BUTTON_NAME and callback.data != 'Поменять направление':
            Student.query_.get(chat_id=callback.message.chat.id)
            student: Student = Student.query_.perform_fetch()

            student.profession = callback.data
            student.save()

            await callback.answer('Выбранное направление сохранено')
            await state.update_data(
                language=student.language,
                russian_nationality=student.russian_nationality,
                study_degree=student.study_degree,
                study_form=student.study_form,
                profession=student.profession
            )


class FullInfoState(State):
    """ Этап, на котором показывается вся информация, которую заполнил пользователь """

    text = 'Язык: {language}\n' \
           'Гражданин РФ: {russian_nationality}\n' \
           'Степень обучения: {study_degree}\n' \
           'Форма обучения: {study_form}\n' \
           'Направление: {profession}\n' \
           '\nЕсли все правильно, жми кнопку готово.\n' \
           'Мы поможем тебе с поступлением и ответим на все вопросы!)'
    keyboard_class = FullInfoKeyboard

    def get_text(self, state: dict):
        state.setdefault('language', '')
        state.setdefault('russian_nationality', '')
        state.setdefault('study_degree', '')
        state.setdefault('study_form', '')
        state.setdefault('professioin', '')
        return self.text.format(**state)
