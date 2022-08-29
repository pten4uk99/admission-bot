from aiogram import types
from aiogram.dispatcher import FSMContext

from architecture.base import State
from architecture.handlers.base import CallbackHandler
from config import BACK_BUTTON_NAME


class StateCallbackHandler(CallbackHandler):
    """ Обработчик, который срабатывает в конце обработки каждого State """

    async def __last_callback(self, callback: types.CallbackQuery, state: FSMContext):
        data = await state.get_data()

        text = f'Привет, будущий {data.get("profession", "")}!\n' \
               'Срок обучения: %4 года%\n' \
               'Бюджетных мест 10\n' \
               'В т.ч. по квоте 2\n' \
               'Платная основа 20\n' \
               '%Очное творческое испытание (кликабельная, вставляем сюда ссылку  https://www.gikit.ru/sites/default/files/ogpage_files/2021/10/Programma_Akterskoe.pdf на программу вступительного испытания)%\n' \
               'Минимальные баллы ЕГЭ для поступления:\n' \
               'Русский  40 баллов\n' \
               'Литература 39 баллов\n' \
               'Стоимость учебы на платной основе: 354000р.\n' \
               '%Ваш руководитель творческой мастерской: ФИО https://www.gikit.ru/page/2022/74019 (фио кликабельная ссылка)%\n' \
               '\nМы будем присылать уведомления о важных сроках, документах, экзаменах, чтобы ты точно ничего важного не упустил и точно поступил к нам!\n' \
               '\nТак же мне можно задать любой вопрос по поводу поступления и я постараюсь тебе на него ответить. Пиши прямо в чат, я готов :)\n'

        await callback.message.edit_text(text=text, reply_markup=None)

    async def handler(self, callback: types.CallbackQuery, state: FSMContext):
        if callback.data == BACK_BUTTON_NAME or callback.data == 'Поменять направление':
            next_state_name = await self.states_group.previous()
        else:
            next_state_name = await self.states_group.next()

        for state_ in self.states_group.states:
            state_: State
            if state_.state == next_state_name:
                data = await state.get_data()
                text = state_.get_text(data)
                await callback.message.edit_text(text=text, reply_markup=state_.get_markup())
                break

        if not (callback.data == BACK_BUTTON_NAME or callback.data == 'Поменять направление'):
            data = await state.get_data()

            if data.get('current_state', None):
                if self.states_group.states[-1].state == data.get('current_state'):
                    await self.__last_callback(callback, state)
                    await state.finish()
                    return

        await state.update_data(current_state=next_state_name)
