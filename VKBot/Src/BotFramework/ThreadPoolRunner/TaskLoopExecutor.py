from Src.BotFramework.Telergam.TelegramListener.LongpollLikeListener import TelegramListener
from Src.BotFramework.Telergam.TelegramWorker import TelegramWorker
from Src.BotFramework.Telergam.Utils.TelegramCore import TelegramCore
from Src.BotFramework.Vkontakte.LongpollHandler import LongPollHandler
from Src.BotFramework.Vkontakte.Vk.Utils.VkApiCore import VkCore
from Src.Controllers.ControllerActioner import ControllerAction


class EventEngine:
    def __init__(self, vk_api_core: VkCore, telegram_api_core: TelegramCore):
        self._controller_action = ControllerAction(vk_api_core, telegram_api_core)
        self._main_thread_vk = LongPollHandler(self._controller_action)
        self._background_thread_telegram = TelegramWorker(self._controller_action)

    async def run_tasks(self):
        #   await self._main_thread_vk.start_handle()
        await self._background_thread_telegram.start_handle()


