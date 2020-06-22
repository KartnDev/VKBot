from enum import IntEnum

import requests
from vk_api import vk_api


class ApiVersion(IntEnum):
    LONG_POLL = 1
    CALLBACK = 2


class VkCore:
    def __init__(self, token: str, access_token: str, version: str = "5.95", api: ApiVersion = ApiVersion.CALLBACK):
        self.token = token
        self.access_token = access_token
        self.version = version
        self.api_listener = api

    @staticmethod
    def _method(method_name: str, args: dict) -> str:
        args = '&'.join('{0}={1}'.format(item, args[item]) for item in args if args[item] is not None)
        _res = requests.get('https://api.vk.com/method/' + method_name + "?" + args)
        if _res.ok:
            return _res.text
        else:
            pass    # TODO log error

    def method(self, method_name: str, args: dict) -> str:
        args.update({'access_token': self.access_token, 'v': self.version})
        return self._method(method_name, args)




