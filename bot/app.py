import logging

from bot import TelegramBot


logging.basicConfig(level=logging.INFO)

bot = TelegramBot()

if __name__ == '__main__':
    bot.start()
 