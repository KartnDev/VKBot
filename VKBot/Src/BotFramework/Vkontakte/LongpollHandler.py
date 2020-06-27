from Src.BotFramework.Utils.ReflectionUtils import methods_with_decorator
from Src.BotFramework.Vkontakte.Vk.SDK.EventSender import VkEvent, VkNewMsgChatEvent
from Src.Controllers.ControllerActioner import ControllerAction
from Src.Controllers.VkControllers.AnyController import AnyController
from Src.Controllers.VkControllers.ChatMsgController import ChatMsgController
from Src.Controllers.VkControllers.UserMsgController import UserMsgController
from Src.BotFramework.Vkontakte.Vk.LongPollListener.LongpollListener import LongPollListener
from Src.Database.UserDbWorker import UserDbWorker


class LongPollHandler:

    def __init__(self, action: ControllerAction):
        self._controller_action = action
        self._vk_action = self._controller_action.vk_action
        self._vk_core = self._vk_action.get_api_core()
        self._vk_listener = LongPollListener(self._vk_core)

        # Handler prepare for any event control context
        self._any_controller = AnyController(self._controller_action)

        self._any_event_handlers = methods_with_decorator(AnyController, "InvokeOnAnyEvent")
        self._any_message_handlers = methods_with_decorator(AnyController, "InvokeOnAnyMessage")

        # Handler prepare for users message control context
        self._user_msg_controller = UserMsgController(self._controller_action)

        self._user_msg_handlers = methods_with_decorator(UserMsgController, "HandleMessage")
        self._user_required_level_handlers = methods_with_decorator(UserMsgController, "RequiredLvl")
        self._user_auth_handlers = methods_with_decorator(UserMsgController, "Authorized")

        # Handler prepare for chats messages control context
        self._chat_controller = ChatMsgController(self._controller_action)

        self._chat_handlers = methods_with_decorator(ChatMsgController, "HandleMessage")
        self._chat_required_level_handlers = methods_with_decorator(ChatMsgController, "RequiredLvl")
        self._chat_auth_handlers = methods_with_decorator(ChatMsgController, "Authorized")

        self._user_wrr = UserDbWorker()

    def _send_call_error_chat(self, chat_id: int, msg: str):
        return self._vk_action.send_message_chat(chat_id=chat_id, message="Call error: " + msg)

    def _send_call_error_to_user(self, user_id: int, msg: str):
        return self._vk_action.send_message(type_id="user_id", id=user_id, message=msg)

    def is_user_registered(self, user_id: int) -> bool:
        return self._user_wrr.contains(user_id)

    async def start_handle(self):
        for event in self._vk_listener.listen():
            print(event)
            if 'type' in event and 'object' in event and 'event_id' in event and 'group_event' in event:
                vk_event = VkEvent(event)
                await self.__handle_any_event(vk_event)
                if vk_event.is_message_new_event():
                    await self.__handle_any_message(vk_event)  # any message
                    obj = event['object']
                    if 'message' in obj:
                        msg = obj['message']
                        if 'from_id' in msg and 'text' in msg and 'peer_id' in msg and 'attachments' in msg:
                            if vk_event.is_message_new_event():
                                new_message_event = vk_event.to_message_new_event()
                                if new_message_event.from_chat():
                                    await self.__find_chat_handler_invoke(new_message_event.to_chat_new_msg_event())
                                elif new_message_event.from_user():
                                    await self.__find_user_msg_handler_invoke(new_message_event.to_user_new_msg_event())

    # region any_handlers

    async def __handle_any_message(self, vk_event: VkEvent):
        for _handler in self._any_message_handlers:
            await getattr(self._any_controller, _handler[0])(vk_event)

    async def __handle_any_event(self, vk_event: VkEvent):
        for _handler in self._any_event_handlers:
            await getattr(self._any_controller, _handler[0])(vk_event)

    # end region any_handlers

    # region chat_handlers

    # TODO test it
    async def __find_chat_handler_invoke(self, chat_event: VkNewMsgChatEvent):
        for _handler in self._chat_handlers:
            if 'msg' in _handler[1]:  # if we wont to explicit use all message
                msg_handle = _handler[1].split('=')[1].replace('\"', '').replace(' ', '').replace('\'', '')

                if msg_handle == chat_event.msg_text:
                    await self.__check_for_chat_annotation_and_invoke(_handler[0], chat_event)
            elif 'first_word' in _handler[1]:  # explicit first-word handler
                word_handle = _handler[1].split("first_word=")[1].replace(' ', '').split(",")[0] \
                    .replace('"', '').replace("'", "")

                words_split = chat_event.msg_text.split(" ")
                if words_split[0] == word_handle:
                    if 'words_length' in _handler[1]:
                        word_require_len = _handler[1].split("words_length=")[1].replace(' ', '').split(",")[0]
                        if int(word_require_len) == len(words_split):
                            await self.__check_for_chat_annotation_and_invoke(_handler[0], chat_event)
                    else:
                        await self.__check_for_chat_annotation_and_invoke(_handler[0], chat_event)

            elif 'first_word' in _handler[1] and _handler in self._user_msg_handlers:
                raise Exception("Cannot explicit cast part of message and message in one expression!")
            break

    async def __check_for_chat_annotation_and_invoke(self, fn_name: str, chat_event: VkNewMsgChatEvent):
        if fn_name[0] in list(item[0] for item in self._chat_auth_handlers):
            await self.__invoke_auth_handler(fn_name, chat_event)

        elif fn_name[0] in list(item[0] for item in self._chat_required_level_handlers):
            await self.__invoke_required_lvl_handler(fn_name, chat_event)

        else:
            await self.__invoke_base_handler(fn_name, chat_event)

    async def __invoke_auth_handler(self, fn_name: str, chat_event: VkNewMsgChatEvent):
        if self.is_user_registered(chat_event.msg_from):
            await getattr(self._chat_controller, fn_name)(chat_event)
        else:
            self._send_call_error_chat(chat_event.msg_peer_id - int(2E9),  # TODO refactor it
                                       """комманда доступна только для 
                                          зарегестрированных 
                                          пользователей""")

    async def __invoke_required_lvl_handler(self, fn_name: str, chat_event: VkNewMsgChatEvent):
        curr_u_lvl = self._user_wrr.first_or_default(chat_event.msg_from)
        if curr_u_lvl is not None:
            curr_u_lvl = curr_u_lvl[1]
        else:
            self._send_call_error_chat(chat_event.msg_peer_id - int(2E9),  # TODO refactor it
                                       """комманда доступна только для 
                                       зарегестрированных 
                                       пользователей c повышенным уровнем доступа""")
        lvl_handle = [handler_item for i, handler_item in enumerate(self._chat_required_level_handlers)
                      if handler_item[0] == fn_name][0]
        needed_lvl = int(lvl_handle[1].split('=')[1])
        if curr_u_lvl >= needed_lvl:
            await getattr(self._chat_controller, fn_name)(chat_event)
        else:
            self._send_call_error_chat(chat_event.msg_peer_id - int(2E9),  # TODO refactor it
                                       """Нет доступа к команде: required lvl = {0},
                                            {1} taken, {0} > {1}""".format(needed_lvl,
                                                                           curr_u_lvl))

    async def __invoke_base_handler(self, fn_name: str, chat_event: VkNewMsgChatEvent):
        await getattr(self._chat_controller, fn_name)(chat_event)

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

    async def __check_for_user_annotation_and_invoke(self, fn_name: str, chat_event: VkNewMsgChatEvent):

        if chat_event.msg_text in list(item[0] for item in self._user_auth_handlers):
            await self.__invoke_auth_handler_user(fn_name, chat_event)

        elif fn_name in list(item[0] for item in self._user_required_level_handlers):
            await self.__invoke_required_lvl_handler_user(fn_name, chat_event)

        else:
            await self.__invoke_base_handler_user(fn_name, chat_event)

    async def __invoke_auth_handler_user(self, fn_name: str, chat_event: VkNewMsgChatEvent):
        if self._user_wrr.contains(chat_event.msg_from):
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
                                                                  "attachment": message['attachments']}, message)
            await getattr(self._user_msg_controller, handler_handlable_msg[0])(user_msg_event)
        else:
            self._send_call_error_to_user(user_id, """Нет доступа к команде: required lvl = {0},
                                            {1} taken, {0} > {1}""".format(needed_lvl, curr_u_lvl))

    async def __invoke_base_handler_user(self, user_id: int, message: dict, handler_handlable_msg: (str, str)):
        user_msg_event = UserEventSender(message['from_id'], {"message": message['text'],
                                                              "attachment": message['attachments']}, message)
        await getattr(self._user_msg_controller, handler_handlable_msg[0])(user_msg_event)

    # region end user_messages_handler
