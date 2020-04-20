from BotFramework.EventSender import ChatEventSender
from BotFramework.SDK import HandleMessage, RequiredLvl, Authorized
from BotFramework.VkAction import VkAction


class ChatMsgController:

    def __getattr__(self, item):
        return getattr(item)

    def __init__(self, vk_action: VkAction):
        self.vk = vk_action

    @Authorized()
    @RequiredLvl(lvl=10)
    @HandleMessage(msg="!Hello")
    def handle_name(self, event_sender: ChatEventSender):
        self.vk.send_message_chat(event_sender.chat_id, "ИДИ НАХУЙ!")
        print(event_sender.chat_id)
        print(event_sender.user_id)
        print(event_sender.event['message'])
        print(event_sender.event['attachment'])

    @Authorized()
    @HandleMessage(msg="!Bye")
    def retw_TO(self, event_sender: ChatEventSender):
        self.vk.send_message('Hello from bot')
        print(event_sender.chat_id)
        print(event_sender.user_id)
        print(event_sender.event['message'])
        print(event_sender.event['attachment'])
