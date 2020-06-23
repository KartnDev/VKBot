from Src.BotFramework.Telergam.TelegramListener.LongpollLikeListener import TelegramListener
from Src.BotFramework.Telergam.Utils.TelegramCore import TelegramCore
from Src.BotFramework.Vkontakte.LongpollHandler import LongPollHandler
from Src.BotFramework.Vkontakte.Vk.Utils.VkApiCore import VkCore


class EventEngine:
    def __init__(self, vk_api_core: VkCore, telegram_api_core: TelegramCore):
        self._main_thread_vk = LongPollHandler(vk_api_core)
        self._background_thread_telegram = TelegramListener(telegram_api_core)

    async def run_tasks(self):
        await self._main_thread_vk.start_handle()
        await self._background_thread_telegram.start_handle()


