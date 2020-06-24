from Src.BotFramework.Telergam.Sdk import TelegramEvent
from Src.BotFramework.Telergam.Sdk.TelegramAnnotationSDK import HandleMessage
from Src.Controllers.ControllerActioner import ControllerAction


class MsgController:

    def __init__(self, acting: ControllerAction):
        self.acting = acting

    @HandleMessage(msg="hello")
    async def handle_hello(self, event_sender: TelegramEvent):
        print("hello in telegram")