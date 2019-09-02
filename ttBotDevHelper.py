# -*- coding: UTF-8 -*-
import os

from TamTamBot.TamTamBot import TamTamBot
from TamTamBot.utils.lng import set_use_django
from openapi_client import NewMessageBody


class BotDevHelper(TamTamBot):
    @property
    def token(self):
        return os.environ.get('TT_BOT_API_TOKEN')

    @property
    def description(self):
        return 'Этот бот помогает в разработке и управлении ботами.\n\n' \
               'This bot is an helper in the development and management of bots.'

    def receive_text(self, update):
        return bool(self.view_messages(update, [update.message.body.mid], update.link))

    def cmd_handler_vmp(self, update):
        res = None
        if not update.this_cmd_response:  # Это прямой вызов команды, а не текстовый ответ на команду
            if update.cmd_args:  # Если вместе с командой сразу переданы аргументы
                list_id = []
                parts = update.cmd_args.get('c_parts') or []
                if parts:
                    for line in parts:
                        for part in line:
                            list_id.append(str(part))
                if list_id:
                    res = self.view_messages(update, list_id, update.link)
        return bool(res)

    def view_messages(self, update, list_mid, link=None):
        res = False
        msgs = self.msg.get_messages(message_ids=list_mid)
        if msgs:
            for msg in msgs.messages:
                r = self.msg.send_message(NewMessageBody(f'Сообщение {msg.body.mid}:\n`{msg}`'[:NewMessageBody.MAX_BODY_LENGTH], link=link), user_id=update.user_id)
                res = res or r
        return res


if __name__ == '__main__':
    set_use_django(False)
    BotDevHelper().polling()
