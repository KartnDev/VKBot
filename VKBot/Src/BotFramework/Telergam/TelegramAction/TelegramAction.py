import json
import types

from Src.BotFramework.Telergam.Utils.TelegramCore import TelegramCore


class TelegramAction:
    def __init__(self, telegram_core: TelegramCore):
        self._telegram_core = telegram_core

    def get_telegram_core(self) -> TelegramCore:
        return self._telegram_core

    def get_updates_json(self):
        return self._telegram_core.method('getUpdates')

    async def base_send_message_async(self, chat_id: int, message: str):
        return await self._telegram_core.method_async('sendMessage', 'get', {'chat_id': chat_id, 'text': message})

    async def send_message(self, chat_id, text,
                           disable_web_page_preview=None, reply_to_message_id=None, reply_markup=None,
                           parse_mode=None, disable_notification=None, timeout=None):
        """
        Use this method to send text messages. On success, the sent Message is returned.
        :param chat_id:
        :param text:
        :param disable_web_page_preview:
        :param reply_to_message_id:
        :param reply_markup:
        :param parse_mode:
        :param disable_notification:
        :param timeout:
        :return:
        """
        method_url = r'sendMessage'
        payload = {'chat_id': str(chat_id), 'text': text}
        if disable_web_page_preview is not None:
            payload['disable_web_page_preview'] = disable_web_page_preview
        if reply_to_message_id:
            payload['reply_to_message_id'] = reply_to_message_id
        if reply_markup:
            payload['reply_markup'] = self._convert_markup(reply_markup)
        if parse_mode:
            payload['parse_mode'] = parse_mode
        if disable_notification is not None:
            payload['disable_notification'] = disable_notification
        if timeout:
            payload['connect-timeout'] = timeout
        return await self._telegram_core.method_async(method_url, 'post', payload)

    @staticmethod
    def _convert_markup(markup):
        # TODO check for isinstance(markup, types.JsonSerializable): return markup.to_json() else return markup
        return markup.to_json()

    async def send_poll_async(self, chat_id, question, options,
                              is_anonymous=None, type_t=None, allows_multiple_answers=None, correct_option_id=None,
                              explanation=None, explanation_parse_mode=None, open_period=None, close_date=None,
                              is_closed=None,
                              disable_notifications=False, reply_to_message_id=None, reply_markup=None, timeout=None):
        method_url = r'sendPoll'
        payload: dict = {
            'chat_id': str(chat_id),
            'question': question,
            'options': json.dumps(options)}

        if is_anonymous is not None:
            payload['is_anonymous'] = is_anonymous
        if type_t is not None:
            payload['type'] = type_t
        if allows_multiple_answers is not None:
            payload['allows_multiple_answers'] = allows_multiple_answers
        if correct_option_id is not None:
            payload['correct_option_id'] = correct_option_id
        if explanation is not None:
            payload['explanation'] = explanation
        if explanation_parse_mode is not None:
            payload['explanation_parse_mode'] = explanation_parse_mode
        if open_period is not None:
            payload['open_period'] = open_period
        if close_date is not None:
            payload['close_date'] = close_date
        if is_closed is not None:
            payload['is_closed'] = is_closed

        if disable_notifications:
            payload['disable_notification'] = disable_notifications
        if reply_to_message_id is not None:
            payload['reply_to_message_id'] = reply_to_message_id
        if reply_markup is not None:
            payload['reply_markup'] = self._convert_markup(reply_markup)
        if timeout:
            payload['connect-timeout'] = timeout
        return await self._telegram_core.method_async(method_url, payload)
