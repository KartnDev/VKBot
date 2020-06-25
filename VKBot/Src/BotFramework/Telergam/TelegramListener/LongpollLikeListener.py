import asyncio

from Src.BotFramework.Telergam.TelegramAction.TelegramAction import TelegramAction
from Src.BotFramework.Telergam.Utils.TelegramCore import TelegramCore


class TelegramListener(TelegramAction):

    def __init__(self, core: TelegramCore):
        super().__init__(core)

    async def listen(self):
        _res: dict = self.get_updates_json()
        if self.__valid(_res):
            last_update_id = _res['result'][-1]['update_id']
            while True:
                _new_res = self.get_updates_json()
                if last_update_id < _new_res['result'][-1]['update_id']:
                    delta_last = _new_res['result'][-1]['update_id'] - last_update_id
                    if delta_last == 1:
                        yield _new_res['result'][-1]
                    elif delta_last > 1:
                        for item in _new_res['result'][-delta_last:]:
                            yield item
                    last_update_id = _new_res['result'][-1]['update_id']
                await asyncio.sleep(1.5)

    @staticmethod
    def __valid(event: dict, sliced: int = -1) -> bool:
        if 'ok' in event and 'result' in event:
            if event['ok']:
                if isinstance(event['result'], list):
                    if len(event['result']) > 0:
                        last_event = event['result'][sliced]
                        if 'update_id' in last_event:
                            return True
        return False


