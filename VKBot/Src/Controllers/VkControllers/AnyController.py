"""*******************************************************************************************
* THIS CONTROLLER FOR @ANY_EVENT and @ANY_MESSAGE                                            *
* DONT USE IT TOO MUCH                                                                       *
*******************************************************************************************"""
from Src.BotFramework.Vkontakte.Vk.SDK.EventSender import VkEvent
from Src.BotFramework.Vkontakte.Vk.SDK.VkAnnotationSDK import InvokeOnAnyMessage, InvokeOnAnyEvent
from Src.Controllers.ControllerActioner import ControllerAction


class AnyController:

    def __init__(self, acting: ControllerAction):
        self.acting = acting

    @InvokeOnAnyMessage()
    async def handle_vk_msg_and_send_to_telegram(self, event_sender: VkEvent):
        print("new message")

    @InvokeOnAnyEvent()
    async def log_any_event(self, event_sender: VkEvent):
        print("new event")