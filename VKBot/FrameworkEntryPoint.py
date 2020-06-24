import asyncio

from Src.BotFramework.Telergam.Utils.TelegramCore import TelegramCore
from Src.BotFramework.ThreadPoolRunner.TaskLoopExecutor import EventEngine
from Src.BotFramework.Vkontakte.Vk.Utils.VkApiCore import VkCore


async def main_func():
    core = VkCore('', '')
    telegram_core = TelegramCore(':')
    bot_tasks = EventEngine(core, telegram_core)
    await bot_tasks.run_tasks()


if __name__ == '__main__':
    asyncio.run(main_func())


