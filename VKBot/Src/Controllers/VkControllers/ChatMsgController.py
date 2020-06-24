from Src.BotFramework.Vkontakte.Vk.SDK.EventSender import ChatEventSender
from Src.BotFramework.Vkontakte.Vk.SDK.VkAnnotationSDK import *
from Src.Controllers.ControllerActioner import ControllerAction
from Src.Database.Connector import DbConnection, DbConnVersion


class ChatMsgController:

    def __init__(self, acting: ControllerAction):
        self.acting = acting

    @HandleMessage(msg="!Крыса")
    @RequiredLvl(lvl=1)
    async def handle_krisa(self, event_sender: ChatEventSender):
        self.acting.vk_action.send_message_chat(event_sender.chat_id, "САМ ТЫ КРЫСА @id" + str(event_sender.user_id))

    @RequiredLvl(lvl=10)
    @HandleMessage(msg="!Hello")
    async def handle_name(self, event_sender: ChatEventSender):
        print("Сообщение пришло из чата id" + str(event_sender.chat_id))
        print("Сообщение пришло от юзера id" + str(event_sender.user_id))
        print("Текст сообщенияЖ :" + event_sender.event['message'])
        print(event_sender.event['attachment'])

    @RequiredLvl(lvl=2)
    @HandleMessage(msg="!Bye")
    async def handle_bye(self, event_sender: ChatEventSender):
        self.acting.vk_action.send_message_chat(event_sender.chat_id, 'Hello from bot!')

    @Authorized()
    @HandleMessage(msg="!status")
    async def handle_(self, event_sender: ChatEventSender):
        data = DbConnection('localhost', 'KartonBot', 'root', 'zxc123', 3306, DbConnVersion.SYNC)
        print(self.acting.vk_action.send_message_chat(event_sender.chat_id, "Ваш уровень " +
                                                      str(data.select_where('users',
                                                                            {'vk_id': event_sender.user_id})[0][1])))

        print("Сообщение пришло из чата id" + str(event_sender.chat_id))
        print("Сообщение пришло от юзера id" + str(event_sender.user_id))
        print("Текст сообщенияЖ :" + event_sender.event['message'])
        print(event_sender.event['attachment'])

    @HandleMessage(first_word="!ban")
    @RequiredLvl(lvl=1)
    async def handle_partial(self, event_sender: ChatEventSender):
        self.acting.vk_action.send_message_chat(event_sender.chat_id, "2Е40 ОК")

    @HandleMessage(first_word="!unban", words_length=3)
    @RequiredLvl(lvl=1)
    async def handle_partial(self, event_sender: ChatEventSender):
        self.acting.vk_action.send_message_chat(event_sender.chat_id, "2Е41 ОК")

    @HandleMessage(words_length=3, first_word="!un")
    @RequiredLvl(lvl=1)
    async def handle_partial(self, event_sender: ChatEventSender):
        self.acting.vk_action.send_message_chat(event_sender.chat_id, "2Е42 ОК")
