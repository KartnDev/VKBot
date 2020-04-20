from vk_api import vk_api


class VkAction:
    def __init__(self, token: str):
        self._vk_session = vk_api.VkApi(token=token)

    def send_message(self):
        pass

    def send_message_chat(self):
        pass

    def send_message_user(self):
        pass

    def send_sticker(self):
        pass

    def send_attachment(self):
        pass

    def send_picture_by_url(self):
        pass

