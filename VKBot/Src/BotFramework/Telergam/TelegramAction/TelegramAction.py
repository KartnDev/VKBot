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

    async def send_message(self, chat_id: int, text: str,
                           disable_web_page_preview=None, reply_to_message_id: int = None, reply_markup=None,
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

    @staticmethod
    def _convert_input_media_array(array):
        media = []
        files = {}
        for input_media in array:
            # TODO if isinstance(input_media, types.InputMedia):
            media_dict = input_media.to_dict()
            if media_dict['media'].startswith('attach://'):
                key = media_dict['media'].replace('attach://', '')
                files[key] = input_media.media
            media.append(media_dict)
        return json.dumps(media), files

    async def send_poll_async(self, chat_id: int, question: str, options: dict,
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
        return await self._telegram_core.method_async(method_name=method_url, args=payload)

    def send_dice(self, chat_id: int,
                  emoji=None, disable_notification=None, reply_to_message_id: int = None,
                  reply_markup=None, timeout=None):
        method_url = r'sendDice'
        payload = {'chat_id': chat_id}
        if emoji:
            payload['emoji'] = emoji
        if disable_notification is not None:
            payload['disable_notification'] = disable_notification
        if reply_to_message_id:
            payload['reply_to_message_id'] = reply_to_message_id
        if reply_markup:
            payload['reply_markup'] = self._convert_markup(reply_markup)
        if timeout:
            payload['connect-timeout'] = timeout
        return await self._telegram_core.method_async(method_name=method_url, args=payload)

    async def send_photo(self, chat_id: int, photo: any,
                         caption=None, reply_to_message_id=None, reply_markup=None,
                         parse_mode=None, disable_notification=None, timeout=None):
        method_url = r'sendPhoto'
        payload = {'chat_id': chat_id}
        files = None
        if not isinstance(photo, str):
            files = {'photo': photo}
        else:
            payload['photo'] = photo
        if caption:
            payload['caption'] = caption
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
        return await self._telegram_core.method_async(method_name=method_url, args=payload, files=files, method='post')

    async def send_media_group(self, chat_id: int, media,
                               disable_notification=None, reply_to_message_id=None, timeout=None):
        method_url = r'sendMediaGroup'
        media_json, files = self._convert_input_media_array(media)
        payload = {'chat_id': chat_id, 'media': media_json}
        if disable_notification is not None:
            payload['disable_notification'] = disable_notification
        if reply_to_message_id:
            payload['reply_to_message_id'] = reply_to_message_id
        if timeout:
            payload['connect-timeout'] = timeout
        return await self._telegram_core.method_async(method_name=method_url, args=payload,
                                                      method='post' if files else 'get',
                                                      files=files if files else None)

    async def send_location(self, chat_id: int, latitude, longitude,
                            live_period=None, reply_to_message_id: int = None, reply_markup=None,
                            disable_notification=None, timeout=None):
        method_url = r'sendLocation'
        payload = {'chat_id': chat_id, 'latitude': latitude, 'longitude': longitude}
        if live_period:
            payload['live_period'] = live_period
        if reply_to_message_id:
            payload['reply_to_message_id'] = reply_to_message_id
        if reply_markup:
            payload['reply_markup'] = self._convert_markup(reply_markup)
        if disable_notification is not None:
            payload['disable_notification'] = disable_notification
        if timeout:
            payload['connect-timeout'] = timeout
        return await self._telegram_core.method_async(method_name=method_url, args=payload)

    async def edit_message_live_location(self, latitude, longitude, chat_id: int = None, message_id: int = None,
                                         inline_message_id=None, reply_markup=None, timeout=None):
        method_url = r'editMessageLiveLocation'
        payload = {'latitude': latitude, 'longitude': longitude}
        if chat_id:
            payload['chat_id'] = chat_id
        if message_id:
            payload['message_id'] = message_id
        if inline_message_id:
            payload['inline_message_id'] = inline_message_id
        if reply_markup:
            payload['reply_markup'] = self._convert_markup(reply_markup)
        if timeout:
            payload['connect-timeout'] = timeout
        return await self._telegram_core.method_async(method_name=method_url, args=payload)

    async def stop_message_live_location(self, chat_id: int = None, message_id: int = None,
                                         inline_message_id: int = None, reply_markup=None, timeout: int = None):
        method_url = r'stopMessageLiveLocation'
        payload = {}
        if chat_id:
            payload['chat_id'] = chat_id
        if message_id:
            payload['message_id'] = message_id
        if inline_message_id:
            payload['inline_message_id'] = inline_message_id
        if reply_markup:
            payload['reply_markup'] = self._convert_markup(reply_markup)
        if timeout:
            payload['connect-timeout'] = timeout
        return await self._telegram_core.method_async(method_name=method_url, args=payload)

    async def send_venue(self, chat_id: int, latitude, longitude, title, address,
                         foursquare_id=None, disable_notification=None,
                         reply_to_message_id: int = None, reply_markup=None, timeout: int = None):
        method_url = r'sendVenue'
        payload = {'chat_id': chat_id, 'latitude': latitude, 'longitude': longitude, 'title': title, 'address': address}
        if foursquare_id:
            payload['foursquare_id'] = foursquare_id
        if disable_notification is not None:
            payload['disable_notification'] = disable_notification
        if reply_to_message_id:
            payload['reply_to_message_id'] = reply_to_message_id
        if reply_markup:
            payload['reply_markup'] = self._convert_markup(reply_markup)
        if timeout:
            payload['connect-timeout'] = timeout
        return await self._telegram_core.method_async(method_name=method_url, args=payload)

    async def send_contact(self, chat_id: int, phone_number: str, first_name: str,
                           last_name: str = None, disable_notification=None,
                           reply_to_message_id: int = None, reply_markup=None, timeout: int = None):
        method_url = r'sendContact'
        payload = {'chat_id': chat_id, 'phone_number': phone_number, 'first_name': first_name}
        if last_name:
            payload['last_name'] = last_name
        if disable_notification is not None:
            payload['disable_notification'] = disable_notification
        if reply_to_message_id:
            payload['reply_to_message_id'] = reply_to_message_id
        if reply_markup:
            payload['reply_markup'] = self._convert_markup(reply_markup)
        if timeout:
            payload['connect-timeout'] = timeout
        return await self._telegram_core.method_async(method_name=method_url, args=payload)

    async def send_chat_action(self, chat_id: int, action, timeout: int = None):
        method_url = r'sendChatAction'
        payload = {'chat_id': chat_id, 'action': action}
        if timeout:
            payload['connect-timeout'] = timeout
        return await self._telegram_core.method_async(method_name=method_url, args=payload)

    async def send_video(self, chat_id: int, data, duration=None, caption=None, reply_to_message_id: int = None,
                         reply_markup=None, parse_mode: int = None, supports_streaming=None,
                         disable_notification=None, timeout: int = None, thumb=None):
        method_url = r'sendVideo'
        payload = {'chat_id': chat_id}
        files = None
        if not isinstance(data, str):
            files = {'video': data}
        else:
            payload['video'] = data
        if duration:
            payload['duration'] = duration
        if caption:
            payload['caption'] = caption
        if reply_to_message_id:
            payload['reply_to_message_id'] = reply_to_message_id
        if reply_markup:
            payload['reply_markup'] = self._convert_markup(reply_markup)
        if parse_mode:
            payload['parse_mode'] = parse_mode
        if supports_streaming is not None:
            payload['supports_streaming'] = supports_streaming
        if disable_notification is not None:
            payload['disable_notification'] = disable_notification
        if timeout:
            payload['connect-timeout'] = timeout
        if thumb:
            if not isinstance(thumb, str):
                files['thumb'] = thumb
            else:
                payload['thumb'] = thumb
        return await self._telegram_core.method_async(method_name=method_url, args=payload, files=files, method='post')

    async def send_animation(self, chat_id: int, data, duration=None, caption=None, reply_to_message_id: int = None,
                             reply_markup=None, parse_mode: int = None, disable_notification=None, timeout: int = None):
        method_url = r'sendAnimation'
        payload = {'chat_id': chat_id}
        files = None
        if not isinstance(data, str):
            files = {'animation': data}
        else:
            payload['animation'] = data
        if duration:
            payload['duration'] = duration
        if caption:
            payload['caption'] = caption
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

        return await self._telegram_core.method_async(method_name=method_url, args=payload, files=files, method='post')

    
