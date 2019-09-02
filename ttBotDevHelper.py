# -*- coding: UTF-8 -*-
import os

from TamTamBot import CallbackButtonCmd
from TamTamBot.TamTamBot import TamTamBot
from TamTamBot.utils.lng import set_use_django
from openapi_client import NewMessageBody, MessageLinkType, BotCommand, Intent


class BotDevHelper(TamTamBot):
    @property
    def token(self):
        return os.environ.get('TT_BOT_API_TOKEN')

    @property
    def description(self):
        return 'Этот бот помогает в разработке и управлении ботами.\n\n' \
               'This bot is an helper in the development and management of bots.'

    @property
    def about(self):
        return 'Этот бот помогает в разработке и управлении ботами.'

    def get_commands(self):
        # type: () -> [BotCommand]
        commands = [
            BotCommand('start', 'о боте'),
            BotCommand('menu', 'показать меню'),
            BotCommand('vmp', 'показать свойства сообщения'),
        ]
        return commands

    @property
    def main_menu_buttons(self):
        # type: () -> []
        buttons = [
            # Кнопка будет выведена цветом по умолчанию - серым
            [CallbackButtonCmd('О боте', 'start')],
            # Кнопка будет выведена цветом для позитивных действий - синим. Также есть негативная - красная
            [CallbackButtonCmd('Показать свойства сообщения', 'vmp', intent=Intent.POSITIVE)],
        ]

        return buttons

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
            else:  # Вывод запроса для ожидания ответа
                self.msg.send_message(NewMessageBody(f'Перешлите *одно* сообщение канала/чата для показа его свойств:'), user_id=update.user_id)
                update.required_cmd_response = True  # Сообщаем о необходимости ожидания текстового ответа
        else:  # Текстовый ответ команде
            message = update.message
            link = message.link  # Доступ к пересланному сообщению через свойство link
            # Проверим - пересылка ли это.
            if link and link.type == MessageLinkType.FORWARD:
                res = self.view_messages(update, [link.message.mid], update.link)
            else:
                # Выведем сообщение об ошибке и сообщим в коде возврата, что команда не отработала.
                self.msg.send_message(NewMessageBody(f'Ошибка. Необходимо *переслать* сообщение из канала/чата. Повторите, пожалуйста.'), user_id=update.user_id)
                return False

        return bool(res)

    def view_messages(self, update, list_mid, link=None):
        res = False
        msgs = self.msg.get_messages(message_ids=list_mid)
        if msgs:
            # Сравнение количества переданных mid с количеством полученных сообщений
            if len(msgs.messages) < len(list_mid):
                self.msg.send_message(NewMessageBody(
                    f'Не удалось получить все запрошенные сообщения. Проверьте доступ бота @{self.username} к каналам/чатам этих сообщений.', link=update.link
                ), user_id=update.user_id)
                return False
            else:
                for msg in msgs.messages:
                    r = self.msg.send_message(NewMessageBody(f'Сообщение {msg.body.mid}:\n`{msg}`'[:NewMessageBody.MAX_BODY_LENGTH], link=link), user_id=update.user_id)
                    res = res or r
        return res


if __name__ == '__main__':
    set_use_django(False)
    BotDevHelper().polling()
