from Src.BotFramework.Telergam.Sdk.TelegramAnnotationSDK import HandleMessage
from Src.BotFramework.Telergam.Sdk.TelegramEvent import TelegramChatEventSender
from Src.Controllers.ControllerActioner import ControllerAction


class MsgController:

    def __init__(self, acting: ControllerAction):
        self.acting = acting

    @HandleMessage(msg="hello")
    async def handle_hello(self, event_sender: TelegramChatEventSender):
        print("hello in telegram")