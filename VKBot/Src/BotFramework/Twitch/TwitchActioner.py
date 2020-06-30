from Src.BotFramework.Twitch.Helix.HelixEvents import ChannelInfo, StreamInfo
from Src.BotFramework.Twitch.TwitchCore import TwitchCore


class TwitchAction:
    def __init__(self, twitch_api_core: TwitchCore):
        self._twitch_api_core = twitch_api_core

    def get_channel_info(self, broadcaster_id: int or str) -> ChannelInfo:
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

    async def get_channel_info_async(self, broadcaster_id: int or str):
        _res = await self._twitch_api_core.helix_request_async(method_name='channels',
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

    def _search_channels_query(self, query: str):
        return self._twitch_api_core.helix_request(method_name='search/channels', uri_args={'query': query})

    async def _search_channels_query_async(self, query: str):
        return await self._twitch_api_core.helix_request(method_name='search/channels', uri_args={'query': query})

    def get_stream_info(self, channel_name: str) -> StreamInfo:
        _res = self._search_channels_query(channel_name)
        if _res.status_code == 200:
            _res_json = _res.json()
            if 'data' in _res_json:
                query_data = _res_json['data']
                if isinstance(_res_json['data'], list):
                    if len(_res_json['data']) > 0:
                        return StreamInfo(_res_json['data'][0])

    async def get_stream_info_async(self, channel_name: str):
        _res = await self._search_channels_query_async(channel_name)
        if _res.status_code == 200:
            _res_json = _res.json()
            if 'data' in _res_json:
                query_data = _res_json['data']
                if isinstance(_res_json['data'], list):
                    if len(_res_json['data']) > 0:
                        return StreamInfo(_res_json['data'][0])

    def is_channel_online(self, channel_name: str) -> bool:
        return self.get_stream_info(channel_name).is_life

    async def is_channel_online_async(self, channel_name: str):
        info = await self.get_stream_info_async(channel_name)
        return info.is_life

