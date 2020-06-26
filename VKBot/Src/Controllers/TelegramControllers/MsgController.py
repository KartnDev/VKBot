from Src.BotFramework.Telergam.Sdk.TelegramAnnotationSDK import HandleMessage
from Src.BotFramework.Telergam.Sdk.TelegramEvent import TelegramChatEventSender
from Src.Controllers.ControllerActioner import ControllerAction


class MsgController:

    def __init__(self, acting: ControllerAction):
        self.acting = acting

    @HandleMessage(msg="hello")
    async def handle_hello(self, event_sender: TelegramChatEventSender):
        await self.acting.telegram_action.send_message(chat_id=event_sender.chat_id,
                                                       text="hi!",
                                                       reply_to_message_id=event_sender.message_id)

    @HandleMessage(first_word="ban")
    async def handle_ban(self, event_sender: TelegramChatEventSender):
        await self.acting.telegram_action.send_message(event_sender.chat_id, "ban here!")

    @HandleMessage(first_word="unban", words_length=3)
    async def handle_unban(self, event_sender: TelegramChatEventSender):
        await self.acting.telegram_action.send_message(event_sender.chat_id, "unban here!")