import asyncio

from Src.BotFramework.ThreadPoolRunner.TaskLoopExecutor import EventEngine
from Src.Vk.VkApiCore import VkCore


async def main_func():
    core = VkCore('', 'cdefe64cad4dfb777159fed5802a6a85ddc7a29eaa4e7f6e876096a07ce53887baa982487b8883b964f8d')
    bot_tasks = EventEngine(core)
    await bot_tasks.run_tasks()


if __name__ == '__main__':
    asyncio.run(main_func())


