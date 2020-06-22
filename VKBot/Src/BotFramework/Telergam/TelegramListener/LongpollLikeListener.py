import asyncio

from Src.BotFramework.Telergam.TelegramAction.TelegramAction import TelegramAction
from Src.BotFramework.Telergam.Utils.TelegramCore import TelegramCore


class TelegramListener(TelegramAction):

    def __init__(self, core: TelegramCore):
        super().__init__(core)

    async def listen_events(self):
        _res: dict = self.get_updates_json()
        result = self.__valid(_res)

        if result[0]:
            last_update_id = result[1]['update_id']
            while True:
                _new_res = self.__valid(self.get_updates_json())
                if _new_res[0]:
                    if last_update_id < _new_res[1]['update_id']:
                        delta_last = _new_res[1]['update_id'] - last_update_id
                        if delta_last == 1:
                            print(_new_res[1]['message']['text'])
                        elif delta_last > 1:
                            for item in _new_res['result'][-delta_last:]:
                                print(item['message']['text'])
                        last_update_id = _new_res['result'][-1]['update_id']
                    await asyncio.sleep(1)

    @staticmethod
    def __valid(event: dict, sliced: int = -1) -> (bool, dict):
        if 'ok' in event and 'result' in event:
            if event['ok']:
                if isinstance(event['result'], list):
                    if len(event['result']) > 0:
                        last_event = event['result'][sliced]
                        if 'update_id' in last_event:
                            return True, last_event
        return False, None


