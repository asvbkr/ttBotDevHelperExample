# -*- coding: UTF-8 -*-
import os

from TamTamBot.TamTamBot import TamTamBot
from TamTamBot.utils.lng import set_use_django


class BotDevHelper(TamTamBot):
    @property
    def token(self):
        return os.environ.get('TT_BOT_API_TOKEN')

    @property
    def description(self):
        return 'Этот бот помогает в разработке и управлении ботами.\n\n' \
               'This bot is an helper in the development and management of bots.'


if __name__ == '__main__':
    set_use_django(False)
    bot = BotDevHelper()
    bot.polling()
