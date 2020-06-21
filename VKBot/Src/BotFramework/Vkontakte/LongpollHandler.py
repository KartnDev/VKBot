import inspect

from Src.BotFramework.Vkontakte.EventSender import ChatEventSender, UserEventSender
from Src.BotFramework.Vkontakte.VkAction import VkAction
from Src.Controllers.ChatMsgController import ChatMsgController
from Src.Controllers.UserMsgController import UserMsgController
from Src.Vk.LongPollListener.LongpollListener import LongPollListener
from Src.Database.UserDbWorker import UserDbWorker
from Src.Vk.VkApiCore import VkCore


class LongPollHandler:

    def __init__(self, vk_api_core: VkCore):
        self._long_poll = LongPollListener(vk_api_core)
        self._vk_action = VkAction(vk_api_core)

        # Handler prepare for users message control context
        self._user_msg_controller = UserMsgController(self._vk_action)

        self._user_msg_handlers = self._methods_with_decorator(UserMsgController, "HandleMessage")
        self._user_required_level_handlers = self._methods_with_decorator(UserMsgController, "RequiredLvl")
        self._user_auth_handlers = self._methods_with_decorator(UserMsgController, "Authorized")

        # Handler prepare for chats messages control context
        self._chat_controller = ChatMsgController(self._vk_action)

        self._chat_handlers = self._methods_with_decorator(ChatMsgController, "HandleMessage")
        self._chat_required_level_handlers = self._methods_with_decorator(ChatMsgController, "RequiredLvl")
        self._chat_auth_handlers = self._methods_with_decorator(ChatMsgController, "Authorized")

        self._user_wrr = UserDbWorker()

    @staticmethod
    def _methods_with_decorator(controller_name, decorator_name: str) -> [(str, str)]:
        # raise Warning("\"_methods_with_decorator\" Method works with errors! do unit tests and rewrite it")
        source_lines = inspect.getsourcelines(controller_name)[0]
        result = []
        for i, line in enumerate(source_lines):
            line = line.strip()
            if line.split('(')[0].strip() == '@' + decorator_name:
                param = line.split('(')[1].split(')')[0]
                next_line = source_lines[i + 1]
                while '@' in next_line:
                    i += 1
                    next_line = source_lines[i + 1]
                decor_name = next_line.split('def')[1].split('(')[0].strip()
                item = (decor_name, param)
                result.append(item)
        return result

    def _send_call_error_chat(self, chat_id: int, msg: str):
        return self._vk_action.send_message_chat(chat_id=chat_id, message="Call error: " + msg)

    def _send_call_error_to_user(self, user_id: int, msg: str):
        return self._vk_action.send_message(type_id="user_id", id=user_id, message=msg)

    def is_user_registered(self, user_id: int) -> bool:
        return self._user_wrr.contains(user_id)

    async def start_handle(self):
        for event in self._long_poll.listen():
            if 'type' in event and 'object' in event:
                if event['type'] == 'message_new':
                    obj = event['object']
                    if 'message' in obj:
                        msg = obj['message']
                        if 'from_id' in msg and 'text' in msg and 'peer_id' in msg and 'attachments' in msg:
                            if msg['peer_id'] > int(2E9):  # from_chat
                                await self.__find_chat_handler_invoke(msg)
                            elif msg['peer_id'] < int(2E9):  # from user
                                await self.__find_user_msg_handler_invoke(msg)

    # region chat_handlers

    # TODO test it
    async def __find_chat_handler_invoke(self, msg: dict):
        for _handler in self._chat_handlers:
            if 'msg' in _handler[1]:  # if we wont to explicit use all message
                msg_handle = _handler[1].split('=')[1].replace('\"', '').replace(' ', '').replace('\'', '')

                if msg_handle == msg['text']:
                    await self.__check_for_user_annotation_and_invoke(_handler, msg['from_id'], msg)
            elif 'first_word' in _handler[1]:  # explicit first-word handler
                word_handle = _handler[1].split("first_word=")[1].replace(' ', '').split(",")[0] \
                    .replace('"', '').replace("'", "")

                words_split = msg['text'].split(" ")
                if words_split[0] == word_handle:
                    if 'words_length' in _handler[1]:
                        word_require_len = _handler[1].split("words_length=")[1].replace(' ', '').split(",")[0]
                        if int(word_require_len) == len(words_split):
                            await self.__check_for_chat_annotation_and_invoke(_handler, msg['from_id'], msg)
                    else:
                        await self.__check_for_chat_annotation_and_invoke(_handler, msg['from_id'], msg)

            elif 'first_word' in _handler[1] and _handler in self._user_msg_handlers:
                raise Exception("Cannot explicit cast part of message and message in one expression!")
            break

    async def __check_for_chat_annotation_and_invoke(self, handler_handlable_msg: (str, str), user_id: int, message):
        if handler_handlable_msg[0] in list(item[0] for item in self._chat_auth_handlers):
            await self.__invoke_auth_handler(user_id, message, handler_handlable_msg)

        elif handler_handlable_msg[0] in list(item[0] for item in self._chat_required_level_handlers):
            await self.__invoke_required_lvl_handler(user_id, message, handler_handlable_msg)

        else:
            await self.__invoke_base_handler(user_id, message, handler_handlable_msg)

    async def __invoke_auth_handler(self, user_id: int, message: dict, handler_handlable_msg: (str, str)):
        if self.is_user_registered(user_id):
            chat_event = ChatEventSender(message['peer_id'] - int(2E9),
                                         int(message['from_id']),
                                         {"message": message['text'],
                                          "attachment": message['attachments']})
            await getattr(self._chat_controller, handler_handlable_msg[0])(chat_event)
        else:
            self._send_call_error_chat(message['peer_id'] - int(2E9),
                                       """комманда доступна только для 
                                          зарегестрированных 
                                          пользователей""")

    async def __invoke_required_lvl_handler(self, user_id: int, message: dict, handler_handlable_msg: (str, str)):
        curr_u_lvl = self._user_wrr.first_or_default(user_id)
        if curr_u_lvl is not None:
            curr_u_lvl = curr_u_lvl[1]
        else:
            self._send_call_error_chat(message['peer_id'] - int(2E9),
                                       """комманда доступна только для 
                                       зарегестрированных 
                                       пользователей c повышенным уровнем доступа""")
        lvl_handle = [handler_item for i, handler_item in enumerate(self._chat_required_level_handlers)
                      if handler_item[0] == handler_handlable_msg[0]][0]
        needed_lvl = int(lvl_handle[1].split('=')[1])
        if curr_u_lvl >= needed_lvl:
            chat_event = ChatEventSender(message['peer_id'] - int(2E9),
                                         int(message['from_id']),
                                         {"message": message['text'],
                                          "attachment": message['attachments']})
            await getattr(self._chat_controller, handler_handlable_msg[0])(chat_event)
        else:
            self._send_call_error_chat(message['peer_id'] - int(2E9),
                                       """Нет доступа к команде: required lvl = {0},
                                            {1} taken, {0} > {1}""".format(needed_lvl,
                                                                           curr_u_lvl))

    async def __invoke_base_handler(self, user_id: int, message: dict, handler_handlable_msg: (str, str)):
        chat_event = ChatEventSender(message['peer_id'] - int(2E9),
                                     int(message['from_id']),
                                     {"message": message['text'],
                                      "attachment": message['attachments']})
        await getattr(self._chat_controller, handler_handlable_msg[0])(chat_event)

    # region end chat_handlers

    # region for user_messages_handler

    # TODO test it
    async def __find_user_msg_handler_invoke(self, msg: dict):
        for _handler in self._user_msg_handlers:
            if 'msg' in _handler[1]:  # if we wont to explicit use all message
                msg_handle = _handler[1].split('=')[1].replace('\"', '').replace(' ', '').replace('\'', '')

                if msg_handle == msg['text']:
                    await self.__check_for_user_annotation_and_invoke(_handler, msg['from_id'], msg)
            elif 'first_word' in _handler[1]:  # explicit first-word handler
                word_handle = _handler[1].split("first_word=")[1].replace(' ', '').split(",")[0] \
                    .replace('"', '').replace("'", "")

                words_split = msg['text'].split(" ")
                if words_split[0] == word_handle:
                    if 'words_length' in _handler[1]:
                        word_require_len = _handler[1].split("words_length=")[1].replace(' ', '').split(",")[0]
                        if int(word_require_len) == len(words_split):
                            await self.__check_for_user_annotation_and_invoke(_handler, msg['from_id'], msg)
                    else:
                        await self.__check_for_user_annotation_and_invoke(_handler, msg['from_id'], msg)

            elif 'first_word' in _handler[1] and _handler in self._user_msg_handlers:
                raise Exception("Cannot explicit cast part of message and message in one expression!")

    async def __check_for_user_annotation_and_invoke(self, handler_handlable_msg: (str, str), user_id: int, message):

        if handler_handlable_msg[0] in list(item[0] for item in self._user_auth_handlers):
            await self.__invoke_auth_handler_user(user_id, message, handler_handlable_msg)

        elif handler_handlable_msg[0] in list(item[0] for item in self._user_required_level_handlers):
            await self.__invoke_required_lvl_handler_user(user_id, message, handler_handlable_msg)

        else:
            await self.__invoke_base_handler_user(user_id, message, handler_handlable_msg)

    async def __invoke_auth_handler_user(self, user_id: int, message: dict, handler_handlable_msg: (str, str)):
        if self._user_wrr.contains(user_id):
            user_msg_event = UserEventSender(message['from_id'], {"message": message['text'],
                                                                  "attachment": message['attachments']})
            await getattr(self._user_msg_controller, handler_handlable_msg[0])(user_msg_event)

        else:
            self._send_call_error_to_user(user_id, 'комманда доступна только для зарегестрированных пользователей')

    async def __invoke_required_lvl_handler_user(self, user_id: int, message: dict, handler_handlable_msg: (str, str)):
        curr_u_lvl = self._user_wrr.first_or_default(user_id)
        if curr_u_lvl is not None:
            curr_u_lvl = curr_u_lvl[1]
        else:
            self._send_call_error_to_user(user_id, 'комманда доступна только для зарегестрированных ' +
                                          'пользователей c повышенным уровнем доступа')

        lvl_handle = [v for i, v in enumerate(self._user_required_level_handlers)
                      if v[0] == handler_handlable_msg[0]][0]
        needed_lvl = int(lvl_handle[1].split('=')[1])
        if curr_u_lvl >= needed_lvl:
            user_msg_event = UserEventSender(message['from_id'], {"message": message['text'],
                                                                  "attachment": message['attachments']})
            await getattr(self._user_msg_controller, handler_handlable_msg[0])(user_msg_event)
        else:
            self._send_call_error_to_user(user_id, """Нет доступа к команде: required lvl = {0},
                                            {1} taken, {0} > {1}""".format(needed_lvl, curr_u_lvl))

    async def __invoke_base_handler_user(self, user_id: int, message: dict, handler_handlable_msg: (str, str)):
        user_msg_event = UserEventSender(message['from_id'], {"message": message['text'],
                                                              "attachment": message['attachments']})
        await getattr(self._user_msg_controller, handler_handlable_msg[0])(user_msg_event)

    # region end user_messages_handler
