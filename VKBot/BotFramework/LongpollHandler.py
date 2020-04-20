from vk_api import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType


class LongPollHandler:

    def __init__(self, token: str):
        self._vk_session = vk_api.VkApi(token=token.get_vk_token())
        self._session_api = self._vk_session.get_api()
        self._long_poll = VkLongPoll(self._vk_session)

    async def start_handle(self):
        for event in self._long_poll.listen():
            if event.type == VkEventType.MESSAGE_NEW:
                if event.from_chat:
                    pass    # UserController Startup
                if event.from_user:
                    pass    # ChatController Startup
