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

    def _send_call_error_chat(self, chat_id: int, msg: str):
        return self._vk_action.send_message_chat(chat_id=chat_id, message="Call error: " + msg)

    def _send_call_error_to_user(self, user_id: int, msg: str):
        return self._vk_action.send_message(type_id="user_id", id=user_id, message=msg)

    async def start_handle(self):
        for event in self._long_poll.listen():
            if 'type' in event and 'object' in event:
                if event['type'] == 'message_new':
                    msg = event['object']
                    if 'from_id' in msg and 'text' in msg and 'peer_id' in msg and 'attachments' in msg:
                        if msg['peer_id'] > int(2E9):  # from_chat
                            await self.__find_chat_handler_invoke(msg)
                        elif msg['peer_id'] < int(2E9):
                            await self.__find_user_msg_handler_invoke(msg)

    async def __find_chat_handler_invoke(self, msg: dict):
        for _handler in self._chat_handlers:
            msg_handle = _handler[1].split('=')[1].replace('\"', '').replace(' ', '').replace('\'', '')
            if msg_handle == msg['text']:
                current_vk_u = msg['from_id']
                # for AUTH ONLY COMMANDS
                if _handler[0] in list(item[0] for item in self._chat_auth_handlers):
                    if self._user_wrr.contains(current_vk_u):
                        chat_event = ChatEventSender(msg['peer_id'] - int(2E9),
                                                     int(msg['from_id']),
                                                     {"message": msg['text'],
                                                      "attachment": msg['attachments']})
                        await getattr(self._chat_controller, _handler[0])(chat_event)
                        break  # Here goes next loop
                    else:
                        self._send_call_error_chat(msg['peer_id'] - int(2E9),
                                                   """комманда доступна только для 
                                                   зарегестрированных 
                                               пользователей""")
                        break  # Here goes next loop
                # for Level - required COMMANDS
                if _handler[0] in list(item[0] for item in self._chat_required_level_handlers):
                    curr_u_lvl = self._user_wrr.first_or_default(current_vk_u)
                    if curr_u_lvl is not None:
                        curr_u_lvl = curr_u_lvl[1]
                    else:
                        self._send_call_error_chat(msg['peer_id'] - int(2E9),
                                                   """комманда доступна только для 
                                                   зарегестрированных 
                                                   пользователей c повышенным уровнем доступа""")
                        break
                    lvl_handle = [handler_item for i, handler_item in enumerate(self._chat_required_level_handlers)
                                  if handler_item[0] == _handler[0]][0]
                    needed_lvl = int(lvl_handle[1].split('=')[1])
                    if curr_u_lvl >= needed_lvl:
                        chat_event = ChatEventSender(msg['peer_id'] - int(2E9),
                                                     int(msg['from_id']),
                                                     {"message": msg['text'],
                                                      "attachment": msg['attachments']})
                        await getattr(self._chat_controller, _handler[0])(chat_event)
                    else:
                        self._send_call_error_chat(msg['peer_id'] - int(2E9),
                                                   """Нет доступа к команде: required lvl = {0},
                                                        {1} taken, {0} > {1}""".format(needed_lvl,
                                                                                       curr_u_lvl))
                        break  # Here goes next loop
                # NORMAL CASUAL COMMANDS
                else:
                    chat_event = ChatEventSender(msg['peer_id'] - int(2E9),
                                                 int(msg['from_id']),
                                                 {"message": msg['text'],
                                                  "attachment": msg['attachments']})
                    await getattr(self._chat_controller, _handler[0])(chat_event)

    async def __find_user_msg_handler_invoke(self, msg: dict):
        for _handler in self._user_msg_handlers:
            msg_handle = _handler[1].split('=')[1].replace('\"', '').replace(' ', '').replace('\'', '')

            if msg_handle == msg['text']:
                current_vk_u = msg['from_id']
                # for AUTH ONLY COMMANDS
                if _handler[0] in list(item[0] for item in self._user_auth_handlers):
                    if self._user_wrr.contains(current_vk_u):
                        user_msg_event = UserEventSender(msg['from_id'], {"message": msg['text'],
                                                                          "attachment": msg['attachments']})
                        await getattr(self._user_msg_controller, _handler[0])(user_msg_event)
                        break  # Here goes next loop
                    else:
                        self._send_call_error_chat(msg['peer_id'] - int(2E9),
                                                   """комманда доступна только для 
                                                      зарегестрированных 
                                                      пользователей""")
                        break  # Here goes next loop
                # for Level - required COMMANDS
                if _handler[0] in list(item[0] for item in self._user_required_level_handlers):
                    curr_u_lvl = self._user_wrr.first_or_default(current_vk_u)
                    if curr_u_lvl is not None:
                        curr_u_lvl = curr_u_lvl[1]
                    else:
                        self._send_call_error_chat(msg['peer_id'] - int(2E9),
                                                   """комманда доступна только для 
                                                      зарегестрированных 
                                                      пользователей c повышенным уровнем доступа""")
                        break
                    lvl_handle = [v for i, v in enumerate(self._user_required_level_handlers)
                                  if v[0] == _handler[0]][0]
                    needed_lvl = int(lvl_handle[1].split('=')[1])
                    if curr_u_lvl >= needed_lvl:
                        user_msg_event = UserEventSender(msg['from_id'], {"message": msg['text'],
                                                                          "attachment": msg['attachments']})
                        await getattr(self._chat_controller, _handler[0])(user_msg_event)
                    else:
                        self._send_call_error_chat(msg['peer_id'] - int(2E9),
                                                   """Нет доступа к команде: required lvl = {0},
                                                        {1} taken, {0} > {1}""".format(needed_lvl,
                                                                                       curr_u_lvl))
                        break  # Here goes next loop
                # NORMAL CASUAL COMMANDS
                else:
                    user_msg_event = UserEventSender(msg['from_id'], {"message": msg['text'],
                                                                      "attachment": msg['attachments']})
                    await getattr(self._chat_controller, _handler[0])(user_msg_event)



    @staticmethod
    def _methods_with_decorator(controller_name, decorator_name: str) -> list:
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
