from aiogram import types

from architecture.base import BaseArchitecture
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
    
    def get_message_to_stage(self, message_text: str = None,
                             message_markup: types.InlineKeyboardMarkup = None) -> callable:
        async def message_to_next_stage(message: types.Message):
            if message_text is not None:
                if message.from_user.is_bot:
                    await message.edit_text(message_text, reply_markup=message_markup)
                else:
                    await message.delete()
                    await message.answer(message_text, reply_markup=message_markup)
    
        return message_to_next_stage


if __name__ == '__main__':
    pass
