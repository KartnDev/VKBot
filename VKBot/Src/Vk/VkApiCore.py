from enum import IntEnum


class ApiVersion(IntEnum):
    LONG_POLL = 1
    CALLBACK = 2


class VkCore:
    def __init__(self, token: str, access_token: str, version: str = "5.95", api: ApiVersion = ApiVersion.CALLBACK):
        self.token = token
        self.access_token = access_token
        self.version = version
        self.api_listener = api

    def get_long_poll_server(self):
        pass
