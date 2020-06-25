from Src.BotFramework.Telergam.Sdk.TelegramAnnotationSDK import InvokeOnAnyMessage, InvokeOnAnyEvent
from Src.BotFramework.Telergam.Sdk.TelegramEvent import TelegramChatEventSender
from Src.Controllers.ControllerActioner import ControllerAction


class AnyTelegramController:

    def __init__(self, acting: ControllerAction):
        self.acting = acting

    @InvokeOnAnyMessage()
    async def handle_hello(self, event_sender: dict):
        print("message new")

    @InvokeOnAnyEvent()
    async def handle_hello(self, event_sender: dict):
        print("event new")