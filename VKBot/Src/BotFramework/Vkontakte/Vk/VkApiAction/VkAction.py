import logging
import random

from Src.BotFramework.Vkontakte.Vk.Utils.VkApiCore import VkCore


class VkAction:
    def __init__(self, vk_api_core: VkCore):
        self._vk_api_core = vk_api_core

    def send_message(self, type_id, id: int, message: str = None, attachment=None, keyboard=None):
        try:
            return self._vk_api_core.method('messages.send', {type_id: id, 'message': message,
                                                             'random_id': random.randint(-2147483648, +2147483648),
                                                             'attachment': attachment,
                                                             'keyboard': keyboard})
        except Exception as ex:
            logging.info(ex)
            return {"Error": 1}

    def send_message_chat(self, chat_id: int, message: str = None, attachment=None, keyboard=None):
        return self.send_message('chat_id', chat_id, message, attachment, keyboard)

    def send_message_user(self, user_id: int, message: str = None, attachment=None, keyboard=None):
        return self.send_message('user_id', user_id, message, attachment, keyboard)

    def send_sticker(self):
        pass

    def send_attachment(self):
        pass

    def send_picture_by_url(self):
        pass

    def get_api_core(self) -> VkCore:
        return self._vk_api_core
