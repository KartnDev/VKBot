from Src.BotFramework.Telergam.TelegramListener.LongpollLikeListener import TelegramListener
from Src.BotFramework.Utils.ReflectionUtils import methods_with_decorator
from Src.Controllers.ControllerActioner import ControllerAction
from Src.Controllers.TelegramControllers.MsgController import MsgController


class TelegramWorker:
    def __init__(self, action: ControllerAction):
        self._controller_action = action
        self._telegram_action = action.telegram_action
        self._telegram_core = self._telegram_action.get_telegram_core()
        self._telegram_listener = TelegramListener(self._telegram_core)

        # Handler prepare for any event control context
        # TODO any handler here

        # Handler prepare for message control context

        self._user_msg_controller = MsgController(self._controller_action)

        self._user_msg_handlers = methods_with_decorator(MsgController, "HandleMessage")

    async def start_handle(self):
        async for event in self._telegram_listener.listen():
            print(event)
            # self.send_message(event)

