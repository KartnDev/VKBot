from Src.BotFramework.Twitch.Helix.HelixEvents import ChannelInfo
from Src.BotFramework.Twitch.TwitchCore import TwitchCore


class TwitchAction:
    def __init__(self, twitch_api_core: TwitchCore):
        self._twitch_api_core = twitch_api_core

    def get_channel_info(self, broadcaster_id: int or str):
        _res = self._twitch_api_core.helix_request(method_name='channels',
                                                   uri_args={'broadcaster_id': broadcaster_id})
        _res_json: dict = _res.json()
        if _res.status_code == 200:
            if 'data' in _res_json:
                return ChannelInfo(_res_json['data'][0])
            else:
                print('no data in response')
        elif _res.status_code == 400:
            print("missing query params")
        elif _res.status_code == 500:
            print('Internal Server Error; Failed to get channel information')




