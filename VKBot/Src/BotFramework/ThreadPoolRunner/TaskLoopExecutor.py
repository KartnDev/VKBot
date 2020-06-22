from Src.BotFramework.Vkontakte.LongpollHandler import LongPollHandler
from Src.BotFramework.Vkontakte.Vk.Utils.VkApiCore import VkCore


class EventEngine:
    def __init__(self, vk_api_core: VkCore):
        self._vk_core = vk_api_core
        self._main_thread_vk = LongPollHandler(vk_api_core)

    async def run_tasks(self):
        await self._main_thread_vk.start_handle()



