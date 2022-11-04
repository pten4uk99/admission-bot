from architecture.base import Keyboard
from config import BACK_BUTTON_NAME


class SelectLanguageKeyboard(Keyboard):
    buttons_names = [
        'Русский',
        'English',
        '中国人',
    ]


class NationalityKeyboard(Keyboard):
    buttons_names = [
        'Да',
        'Нет',
        BACK_BUTTON_NAME
    ]


class StudyFormKeyboard(Keyboard):
    buttons_names = [
        'Очная',
        'Очно-заочная',
        'Заочная',
        BACK_BUTTON_NAME
    ]


class StudyDegreeKeyboard(Keyboard):
    buttons_names = [
        'Бакалавриат/Специалитет',
        'Магистратура',
        'Аспирантура',
        BACK_BUTTON_NAME
    ]


class SelectCourseKeyboard(Keyboard):
    buttons_names = [
        'Режиссер игрового кино',
        'Звукорежиссер АВИ',
        'Искусствовед',
        'Драматург',
        'Актер театра и кино',
        'Киновед',
        BACK_BUTTON_NAME
    ]


class FullInfoKeyboard(Keyboard):
    buttons_names = [
        'Поменять направление',
        'Готово'
    ]
