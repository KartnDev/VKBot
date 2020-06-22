import asyncio

from Src.BotFramework.Telergam.TelegramAction.TelegramAction import TelegramAction
from Src.BotFramework.Telergam.Utils.TelegramCore import TelegramCore


class TelegramListener(TelegramAction):

    def __init__(self, core: TelegramCore):
        super().__init__(core)

    async def listen_events(self):
        _res: dict = self.get_updates_json()
        if 'ok' in _res and 'result' in _res:
            if _res['ok']:
                if 'update_id' in _res['result'][-1]:
                    last_update_id = _res['result'][-1]['update_id']
                    while True:
                        _new_res = self.get_updates_json()
                        if last_update_id < _new_res['result'][-1]['update_id']:

                            delta_last = _new_res['result'][-1]['update_id'] - last_update_id
                            if delta_last == 1:
                                print(_new_res['result'][-1]['message']['text'])
                            elif delta_last > 1:
                                for item in _new_res['result'][-delta_last:]:
                                    print(item['message']['text'])
                            last_update_id = _new_res['result'][-1]['update_id']
                        await asyncio.sleep(1)






