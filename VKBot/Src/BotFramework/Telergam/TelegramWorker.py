from Src.BotFramework.Telergam.TelegramListener.LongpollLikeListener import TelegramListener
from Src.BotFramework.Telergam.Utils.TelegramCore import TelegramCore


class TelegramWorker:
    def __init__(self, core: TelegramCore):
        self.telegram_listener = TelegramListener(core)

        #load handlers

    async def start_handle(self):
        async for event in self.telegram_listener.listen():
            print(event)
            # self.send_message(event)

