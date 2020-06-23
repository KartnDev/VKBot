"""*******************************************************************************************
* THIS CONTROLLER FOR @ANY_EVENT and @ANY_MESSAGE                                            *
* DONT USE IT TOO MUCH                                                                       *
*******************************************************************************************"""
from Src.BotFramework.Vkontakte.Vk.SDK.EventSender import VkEventSender
from Src.BotFramework.Vkontakte.Vk.SDK.SDK import InvokeOnAnyMessage, InvokeOnAnyEvent
from Src.Controllers.ControllerActioner import ControllerAction


class AnyController:

    def __init__(self, acting: ControllerAction):
        self.acting = acting

    @InvokeOnAnyMessage()
    async def handle_vk_msg_and_send_to_telegram(self, event_sender: VkEventSender):
        self.acting.telegram_action.send_message(1123213213213, "3123213")

    @InvokeOnAnyEvent()
    async def log_any_event(self, event_sender: VkEventSender):
        print(event_sender.all_data_event)