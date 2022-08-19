from aiogram import types


class CallbackMessageGenerator:
    count = 0

    def __init__(self, message_text: str = None,
                 message_markup: types.InlineKeyboardMarkup = None):
        self.__class__.count += 1
        self.count = self.__class__.count
        self.message_text = message_text
        self.message_markup = message_markup
        # print(f'Объект {self.count}', message_text, message_markup)

    def __str__(self):
        return f'<Объект {self.__class__.__name__} {self.count} {self.message_text} {self.message_markup}>'

    async def __call__(self, message: types.Message):
        if self.message_text is not None:
            if message.from_user.is_bot:
                await message.edit_text(self.message_text, reply_markup=self.message_markup)
            else:
                await message.delete()
                await message.answer(self.message_text, reply_markup=self.message_markup)
