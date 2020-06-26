import json

import requests
import requests_async


class TelegramCore:
    def __init__(self, token: str):
        self.token = token
        self.proxy = None
        self.session = None

        self.API_URL = None
        self.FILE_URL = None

        self.CONNECT_TIMEOUT = 3.5
        self.READ_TIMEOUT = 9999

        self.CUSTOM_SERIALIZER = None

        self.ENABLE_MIDDLEWARE = False

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

    async def method_async(self, method_name: str, method: str = 'get', args: dict = None):
        if args is not None:
            args_line = '&'.join('{0}={1}'.format(item, args[item]) for item in args if args[item] is not None)
            url = "https://api.telegram.org/bot{0}/{1}?{2}".format(self.token, method_name, args_line)
        else:
            url = "https://api.telegram.org/bot{0}/{1}".format(self.token, method_name)
        if method == 'get':
            _res = await requests_async.get(url)
        elif method == 'post':
            _res = await requests_async.post(url=url, json=json.dumps(args))
        else:
            raise Exception("Method should be post or get!")

        if _res.ok:
            return _res.json()
        else:
            pass  # TODO log error

    async def make_method_async(self, method_name, method='get', params=None):
        """
        Makes a request to the Telegram API.
        :param method_name: Name of the API method to be called. (E.g. 'getUpdates')
        :param method: HTTP method to be used. Defaults to 'get'.
        :param params: Optional parameters. Should be a dictionary with key-value pairs.
        :return: The result parsed to a JSON dictionary.
        """
        if self.API_URL is None:
            request_url = "https://api.telegram.org/bot{0}/{1}".format(self.token, method_name)
        else:
            request_url = self.API_URL.format(self.token, method_name)

        # TODO logger debug Request: method={0} url={1} params={2} files={3} .format(method, request_url, params, files
        read_timeout = self.READ_TIMEOUT
        connect_timeout = self.CONNECT_TIMEOUT
        if params:
            if 'timeout' in params:
                read_timeout = params.pop('timeout') + 10
            if 'connect-timeout' in params:
                connect_timeout = params.pop('connect-timeout') + 10
        result = await requests_async.request(method, request_url, params=params,
                                              timeout=(connect_timeout, read_timeout), proxies=self.proxy)
        # TODO logger.debug("The server returned: '{0}'".format(result.text.encode('utf8')))
        return self._check_result(method_name, result)['result']

    @staticmethod
    def _check_result(method_name, result):
        """
        Checks whether `result` is a valid API response.
        A result is considered invalid if:
            - The server returned an HTTP response code other than 200
            - The content of the result is invalid JSON.
            - The method call was unsuccessful (The JSON 'ok' field equals False)
        :raises ApiException: if one of the above listed cases is applicable
        :param method_name: The name of the method called
        :param result: The returned result of the method request
        :return: The result parsed to a JSON dictionary.
        """
        if result.status_code != 200:
            msg = 'The server returned HTTP {0} {1}. Response body:\n[{2}]' \
                .format(result.status_code, result.reason, result.text.encode('utf8'))
            raise Exception(msg, method_name, result)

        try:
            result_json = result.json()
        except Exception as ex:
            msg = 'The server returned an invalid JSON response. Response body:\n[{0}]' \
                .format(result.text.encode('utf8'))
            raise Exception(msg, method_name, result)

        if not result_json['ok']:
            msg = 'Error code: {0} Description: {1}' \
                .format(result_json['error_code'], result_json['description'])
            raise Exception(msg, method_name, result)

        return result_json
