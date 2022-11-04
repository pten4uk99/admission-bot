from aiogram.dispatcher.filters.state import StatesGroup

from architecture.stages.register_user.stages import *
from architecture.stages.subscription_send.stages import *


class RegisterUserStateGroup(StatesGroup):
    select_language = SelectLanguageState()
    nationality = NationalityState()
    study_degree = StudyDegreeState()
    study_form = StudyFormState()
    select_course = SelectCourseState()
    full_info = FullInfoState()


class SubscriptionSendStateGroup(StatesGroup):
    study_degree = StudyDegreeSendState()
    study_form = StudyFormSendState()
    select_course = SelectCourseSendState()
    finish_state = FinishSendState()
