from enum import IntEnum

import requests as requests
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
        args = '&'.join('{0}={1}'.format(item, args[item]) for item in args)
        _res = requests.get('https://api.vk.com/method/' + method_name + "?" + args)
        if _res.status_code == 'ok':
            return _res.text

    def method(self, method_name: str, args: dict) -> str:
        args.update({'access_token': self.access_token, 'v': self.version})
        return self._method(method_name, args)








vk = VkCore('', 'cdefe64cad4dfb777159fed5802a6a85ddc7a29eaa4e7f6e876096a07ce53887baa982487b8883b964f8d')
print(vk.get_long_poll_server())
