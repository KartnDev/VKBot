from Src.BotFramework.Vkontakte import VkAction
from Src.BotFramework.Vkontakte.EventSender import UserEventSender
from Src.BotFramework.Vkontakte.SDK import HandleMessage


class UserMsgController:

    def __getattr__(self, item):
        return getattr(item)

    def __init__(self, vk_action: VkAction):
        self.vk = vk_action

    @HandleMessage(msg="!привет")
    async def handle_hello(self, event_sender: UserEventSender):
        print("Hello form: " + str(event_sender.user_id))
        self.vk.send_message(type_id="user_id", id=event_sender.user_id, message="Здорово очередняра")

