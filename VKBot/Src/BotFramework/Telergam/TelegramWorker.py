from Src.BotFramework.Telergam.Sdk.TelegramEvent import TelegramChatEventSender
from Src.BotFramework.Telergam.TelegramListener.LongpollLikeListener import TelegramListener
from Src.BotFramework.Utils.ReflectionUtils import methods_with_decorator
from Src.Controllers.ControllerActioner import ControllerAction
from Src.Controllers.TelegramControllers.AnyTelegramController import AnyTelegramController
from Src.Controllers.TelegramControllers.MsgController import MsgController


class TelegramWorker:
    def __init__(self, action: ControllerAction):
        self._controller_action = action
        self._telegram_action = action.telegram_action
        self._telegram_core = self._telegram_action.get_telegram_core()
        self._telegram_listener = TelegramListener(self._telegram_core)

        # Handler prepare for any event control context

        self._any_telegram_controller = AnyTelegramController(self._controller_action)

        self._any_message_handlers = methods_with_decorator(AnyTelegramController, "InvokeOnAnyMessage")
        self._any_event_handlers = methods_with_decorator(AnyTelegramController, "InvokeOnAnyEvent")

        # Handler prepare for message control context

        self._user_msg_controller = MsgController(self._controller_action)

        self._user_msg_handlers = methods_with_decorator(MsgController, "HandleMessage")

    async def start_handle(self):
        async for event in self._telegram_listener.listen():
            await self.__handle_any_event(event)
            if self.__valid(event):
                telegram_event = TelegramChatEventSender(event)
                await self.__find_telegram_msg_handler_invoke(telegram_event)
                await self.__handle_any_message(event)

    async def __handle_any_event(self, event: dict):
        for _handler in self._any_event_handlers:
            await getattr(self._any_telegram_controller, _handler[0])(event)

    async def __handle_any_message(self, event: dict):
        for _handler in self._any_message_handlers:
            await getattr(self._any_telegram_controller, _handler[0])(event)

    async def __find_telegram_msg_handler_invoke(self, telegram_event: TelegramChatEventSender):
        for _handler in self._user_msg_handlers:
            if 'msg' in _handler[1]:  # if we wont to explicit use all message
                msg_handle = _handler[1].split('=')[1].replace('\"', '').replace(' ', '').replace('\'', '')
                if msg_handle == telegram_event.text_msg:
                    await getattr(self._user_msg_controller, _handler[0])(telegram_event)
            elif 'first_word' in _handler[1]:  # explicit first-word handler
                word_handle = _handler[1].split("first_word=")[1].replace(' ', '').split(",")[0] \
                    .replace('"', '').replace("'", "")

                words_split = telegram_event.text_msg.split(" ")
                if words_split[0] == word_handle:
                    if 'words_length' in _handler[1]:
                        word_require_len = _handler[1].split("words_length=")[1].replace(' ', '').split(",")[0]
                        if int(word_require_len) == len(words_split):
                            await getattr(self._user_msg_controller, _handler[0])(telegram_event)
                    else:
                        await getattr(self._user_msg_controller, _handler[0])(telegram_event)

            elif 'first_word' in _handler[1] and _handler in self._user_msg_handlers:
                raise Exception("Cannot explicit cast part of message and message in one expression!")
            break

    @staticmethod
    def __valid(event: dict):
        return 'update_id' in event and \
               'message' in event and \
               'chat' in event and \
               'date' in event and \
                'text' in event






