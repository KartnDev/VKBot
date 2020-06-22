import requests


class TelegramCore:
    def __init__(self, token: str):
        self.token = token

    # TODO do it async
    def method(self, method_name: str, args: dict = None):
        if args is not None:
            args_line = '&'.join('{0}={1}'.format(item, args[item]) for item in args if args[item] is not None)
            url = "https://api.telegram.org/bot{0}/{1}?{2}".format(self.token, method_name, args_line)
        else:
            url = "https://api.telegram.org/bot{0}/{1}".format(self.token, method_name)
        _res = requests.get(url)
        if _res.ok:
            return _res.json()
        else:
            pass  # TODO log error
