from Src.BotFramework.Telergam.TelegramAction.TelegramAction import TelegramAction
from Src.BotFramework.Telergam.Utils.TelegramCore import TelegramCore
from Src.BotFramework.Twitch.TwitchActioner import TwitchAction
from Src.BotFramework.Twitch.TwitchCore import TwitchCore
from Src.BotFramework.Vkontakte.Vk.Utils.VkApiCore import VkCore
from Src.BotFramework.Vkontakte.Vk.VkApiAction.VkAction import VkAction


class ControllerAction(object):
    def __init__(self, vk_core: VkCore, telegram_core: TelegramCore, twitch_core: TwitchCore):
        self._twitch_core = twitch_core
        self._telegram_core = telegram_core
        self._vk_core = vk_core
        self.vk_action = VkAction(vk_core)
        self.telegram_action = TelegramAction(telegram_core)
        self.twitch_action = TwitchAction(twitch_core)