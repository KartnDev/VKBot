from Src.BotFramework import VkAction
from Src.BotFramework.EventSender import ChatEventSender
from Src.BotFramework.SDK import HandleMessage


class ChatMsgController:

    def __getattr__(self, item):
        return getattr(item)

    def __init__(self, vk_action: VkAction):
        self.vk = vk_action

    @HandleMessage(msg="!Крыса")
    def handle_krisa(self, event_sender: ChatEventSender):
        self.vk.send_message_chat(event_sender.chat_id, "САМ ТЫ КРЫСА @id" + str(event_sender.user_id))

    @HandleMessage(msg="!Hello")
    def handle_name(self, event_sender: ChatEventSender):
        self.vk.send_message_chat(event_sender.chat_id, "ИДИ НАХУЙ!")

        print("Сообщение пришло из чата id"+ str(event_sender.chat_id))
        print("Сообщение пришло от юзера id"+ str(event_sender.user_id))
        print("Текст сообщенияЖ :"+ event_sender.event['message'])
        print(event_sender.event['attachment'])

    @HandleMessage(msg="!Bye")
    def ret(self, event_sender: ChatEventSender):
        self.vk.send_message('Hello from bot')

    @HandleMessage
    def on_map_request(self, map_id: int):
        pass