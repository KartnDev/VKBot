import json
import logging
from Src.Vk.VkApiCore import VkCore


class LongPollListener:
    def __init__(self, vk_api_core: VkCore):
        self.core = vk_api_core

    def _get_long_poll_server(self):
        return self.core.method('groups.getLongPollServer', {'group_id': '182157757'})

    def _get_long_poll_data(self) :
        _r_data = self._get_long_poll_server()
        key = None
        server = None
        ts = None
        if _r_data is not None:  # if code was 200 OK
            _map = json.loads(_r_data)
            if 'response' in _map:
                _res = _map['response']
                if 'key' in _res and 'server' in _res and 'ts' in _res:
                    key = _res['key']
                    server = _res['server']
                    ts = _res['ts']
                else:
                    logging.critical("Cannot get one of needed params for server in request vk")
                    raise KeyError('Cannot get one of needed params for server in request vk')
            else:
                logging.critical("Something went wrong.. No response header in str")
                raise ValueError('Something went wrong.. No response header in str')
        else:
            logging.critical("Bad response for vk api")
            raise IOError('Bad response for vk api')
        return key, server, ts

    def _get_long_poll_server_url(self, ts, key, server: str):
        return server.replace('\\', '')


    def listen(self):
        key, ts ,server = self._get_long_poll_data()

        _pattern = {$server}?act=a_check&key={$key}&ts={$ts}&wait=25