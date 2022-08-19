from typing import Callable

from aiogram import types

from architecture.base import BaseArchitecture
from architecture.base.callback_message_generator import CallbackMessageGenerator
from architecture.stages.stages import *


class Architecture(BaseArchitecture):
    stages_classes = [
        StartStage,
        SelectLanguageStage,
        NationalityStage,
        StudyDegreeStage,
        StudyFormStage,
        SelectCourseStage,
        ChangeCourseStage,
    ]


if __name__ == '__main__':
    pass
