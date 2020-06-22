from Src.BotFramework.Vkontakte.Vk.VkApiAction.VkAction import VkAction


class TelegramToVkLinker:

    def __init__(self, vk_action: VkAction, telegram_action):
        self.telegram_action = telegram_action
        self.vk_action = vk_action

    async def entire_telegram_messaging(self, vk_event: dict, client_telegram_chats: list):
        for telegram_chat in client_telegram_chats:
            msg = "{0} в {1}: {2}".format(vk_event['username'], vk_event["chat_id"], vk_event["message"])
            self.telegram_action.send_message_chat(telegram_chat,  msg)

    async def entire_vk_messaging(self, ):
