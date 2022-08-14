from architecture.base.stage import Stage
from .keyboards import *
from ..base import MessageHandlerStage


class StartStage(MessageHandlerStage):
    """ Этап ввода команды /start """
    
    def register_message_handlers(self):
        self.dp.register_message_handler(self._handler, commands=['start'])


class NationalityStage(Stage):
    """ Этап выбора гражданства """
    
    text = "Гражданство РФ?"
    keyboard_class = NationalityKeyboard


class SelectLanguageStage(Stage):
    """ Состояние выбора языка """
    
    text = "Выберите язык/Select Language"
    keyboard_class = SelectLanguageKeyboard


class StudyDegreeStage(Stage):
    """ Состояние выбора степени обучения """
    
    text = 'Привет! Я бот-помощник %Название УЗ%. ' \
           'У меня ты можешь узнать любой ответ на вопрос о поступлении. ' \
           'Я буду уведомлять о важных событиях на протяжении всего процесса поступления. ' \
           'Не отписывайтесь от меня! Выберите степень обучения.'
    keyboard_class = StudyDegreeKeyboard


class StudyFormStage(Stage):
    """ Этап выбора формы обучения """
    
    text = 'Выберите форму обучения'
    keyboard_class = StudyFormKeyboard
    
    
class SelectCourseStage(Stage):
    """ Этап выбора направления """
    
    text = 'Выберите ваше направление'
    keyboard_class = SelectCourseKeyboard
    
    
class ChangeCourseStage(Stage):
    """ Этап смены направления и обработки сообщений """
    
    text = 'Будущий %название направления(берем из тэга)%! ' \
           'Теперь мы будем присылать тебе важные уведомления, ' \
           'так ты не пропустишь ничего важного и точно поступишь к нам!  ' \
           'Ты можешь спросить у меня любой вопрос по поводу поступления и вуза в чат, ' \
           'и я постараюсь тебе на него ответить.'
    keyboard_class = ChangeCourseKeyboard
    
