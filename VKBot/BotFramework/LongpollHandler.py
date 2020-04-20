import inspect

from vk_api import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

from Controllers import ChatMsgController


class LongPollHandler:

    def __init__(self, token: str):
        self._vk_session = vk_api.VkApi(token=token)
        self._session_api = self._vk_session.get_api()
        self._long_poll = VkLongPoll(self._vk_session)

    def start_handle(self):
        for event in self._long_poll.listen():
            if event.type == VkEventType.MESSAGE_NEW:
                if event.from_chat:
                    pass    # UserController Startup
                if event.from_user:
                    pass    # ChatController Startup
                if event.from_group:
                    pass
                if event.from_me:
                    pass

    def _find_def_with(self, msg: str, decorator: str, controller_name: str):
        pass

    @staticmethod
    def _methods_with_decorator(controller_name: str, decorator_name: str):
        source_lines = inspect.getsourcelines(controller_name)[0]
        for i, line in enumerate(source_lines):
            line = line.strip()
            if line.split('(')[0].strip() == '@' + decorator_name:
                param = line.split('(')[1].split(')')[0]
                next_line = source_lines[i+1]
                decor_name = next_line.split('def')[1].split('(')[0].strip()
                yield (decor_name, param)


for name in LongPollHandler._methods_with_decorator(ChatMsgController, "Authorized"):
    print(name)



