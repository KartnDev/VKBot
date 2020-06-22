from Src.BotFramework.Telergam.Utils.TelegramCore import TelegramCore


class TelegramAction:
    def __init__(self, telegram_core: TelegramCore):
        self.telegram_core = telegram_core

    def get_updates_json(self):
        return self.telegram_core.method('getUpdates')


