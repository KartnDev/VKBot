from Src.BotFramework.Vkontakte.Vk.VkApiAction import VkAction
from Src.BotFramework.Vkontakte.Vk.SDK.EventSender import UserEventSender
from Src.BotFramework.Vkontakte.Vk.SDK.SDK import HandleMessage, Authorized, RequiredLvl
from Src.Controllers.ControllerActioner import ControllerAction


class UserMsgController:

    def __init__(self, acting: ControllerAction):
        self.acting = acting

    @Authorized()
    @HandleMessage(msg="!привет")
    async def handle_hello(self, event_sender: UserEventSender):
        print("Hello form: " + str(event_sender.user_id))
        self.acting.vk_action.send_message(type_id="user_id", id=event_sender.user_id, message="Здорово очередняра")

    @Authorized()
    @HandleMessage(msg="!status")
    async def handle_(self, event_sender: UserEventSender):
        self.acting.vk_action.send_message(type_id="user_id", id=event_sender.user_id, message="статус")

    @RequiredLvl(lvl=2)
    @HandleMessage(msg="!Bye")
    async def handle_bye(self, event_sender: UserEventSender):
        self.acting.vk_action.send_message(type_id="user_id", id=event_sender.user_id, message="!Bye очередняра")

    @HandleMessage(first_word="!ban")
    @RequiredLvl(lvl=1)
    async def handle_partial(self, event_sender: UserEventSender):
        self.acting.vk_action.send_message(type_id="user_id", id=event_sender.user_id, message="2E40 OK !ban")

    @HandleMessage(first_word="!unban", words_length=3)
    @RequiredLvl(lvl=1)
    async def handle_partial(self, event_sender: UserEventSender):
        self.acting.vk_action.send_message(type_id="user_id", id=event_sender.user_id, message="2E40 OK !unban")

    @HandleMessage(words_length=3, first_word="!un")
    @RequiredLvl(lvl=1)
    async def handle_partial(self, event_sender: UserEventSender):
        self.acting.vk_action.send_message(type_id="user_id", id=event_sender.user_id, message="2E40 OK !unban")

    @HandleMessage(words_length=3, first_word="!un2")
    @RequiredLvl(lvl=2)
    async def handle_partial_2(self, event_sender: UserEventSender):
        self.acting.vk_action.send_message(type_id="user_id", id=event_sender.user_id, message="2E40 OK !unban")