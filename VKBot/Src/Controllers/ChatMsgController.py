from Src.BotFramework.Vkontakte.EventSender import ChatEventSender
from Src.BotFramework.Vkontakte.VkAction import VkAction
from Src.BotFramework.Vkontakte.SDK import *
from Src.Database.Connector import DbConnection, DbConnVersion


class ChatMsgController:

    def __init__(self, vk_action: VkAction):
        self.vk = vk_action

    @HandleMessage(msg="!Крыса")
    @RequiredLvl(lvl=1)
    def handle_krisa(self, event_sender: ChatEventSender):
        self.vk.send_message_chat(event_sender.chat_id, "САМ ТЫ КРЫСА @id" + str(event_sender.user_id))

    @RequiredLvl(lvl=10)
    @HandleMessage(msg="!Hello")
    def handle_name(self, event_sender: ChatEventSender):
        #print(self.vk.send_message_chat(event_sender.chat_id, "ИДИ НАХУЙ!"))

        print("Сообщение пришло из чата id" + str(event_sender.chat_id))
        print("Сообщение пришло от юзера id" + str(event_sender.user_id))
        print("Текст сообщенияЖ :" + event_sender.event['message'])
        print(event_sender.event['attachment'])

    @RequiredLvl(lvl=2)
    @HandleMessage(msg="!Bye")
    def retw_to(self, event_sender: ChatEventSender):
        self.vk.send_message_chat(event_sender.chat_id, 'Hello from bot!')

    @Authorized()
    @HandleMessage(msg="!status")
    def handle_(self, event_sender: ChatEventSender):
        data = DbConnection('localhost', 'KartonBot', 'root', 'zxc123', 3306, DbConnVersion.SYNC)
        print(self.vk.send_message_chat(event_sender.chat_id, "Ваш уровень " +
                                        str(data.select_where('users', {'vk_id': event_sender.user_id})[0][1])))

        print("Сообщение пришло из чата id" + str(event_sender.chat_id))
        print("Сообщение пришло от юзера id" + str(event_sender.user_id))
        print("Текст сообщенияЖ :" + event_sender.event['message'])
        print(event_sender.event['attachment'])