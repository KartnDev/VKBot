from Src.BotFramework.Telergam.Utils.TelegramCore import TelegramCore


class TelegramAction:
    def __init__(self, telegram_core: TelegramCore):
        self._telegram_core = telegram_core

    def get_telegram_core(self) -> TelegramCore:
        return self._telegram_core

    def get_updates_json(self):
        return self._telegram_core.method('getUpdates')

    async def send_message(self, chat_id: int, message: str):
        return await self._telegram_core.method_async('sendMessage', {'chat_id': chat_id, 'text': message})

    
