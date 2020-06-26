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

    @staticmethod
    def get_method_by_type(data_type: str):
        if data_type == 'document':
            return r'sendDocument'
        if data_type == 'sticker':
            return r'sendSticker'

    @staticmethod
    def _convert_list_json_serializable(results):
        ret = ''
        for r in results:
            # TODO check for isinstance(markup, types.JsonSerializable):
            if True:
                ret = ret + r.to_json() + ','
        if len(ret) > 0:
            ret = ret[:-1]
        return '[' + ret + ']'

    @staticmethod
    def _convert_input_media(media):
        # TODO if isinstance(media, types.InputMedia):
        if True:
            return media._convert_input_media()
        return None, None

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

    async def send_voice(self, chat_id: int, voice, caption=None, duration=None, reply_to_message_id: int = None,
                         reply_markup=None, parse_mode: int = None, disable_notification=None, timeout: int = None):
        method_url = r'sendVoice'
        payload = {'chat_id': chat_id}
        files = None
        if not isinstance(voice, str):
            files = {'voice': voice}
        else:
            payload['voice'] = voice
        if caption:
            payload['caption'] = caption
        if duration:
            payload['duration'] = duration
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

    async def send_video_note(self, chat_id: int, data, duration: int = None, length: int = None, timeout: int = None,
                              reply_to_message_id: int = None, reply_markup=None, disable_notification=None):
        method_url = r'sendVideoNote'
        payload = {'chat_id': chat_id}
        files = None
        if not isinstance(data, str):
            files = {'video_note': data}
        else:
            payload['video_note'] = data
        if duration:
            payload['duration'] = duration
        if length:
            payload['length'] = length
        else:
            payload['length'] = 639  # seems like it is MAX length size
        if reply_to_message_id:
            payload['reply_to_message_id'] = reply_to_message_id
        if reply_markup:
            payload['reply_markup'] = self._convert_markup(reply_markup)
        if disable_notification is not None:
            payload['disable_notification'] = disable_notification
        if timeout:
            payload['connect-timeout'] = timeout
        return await self._telegram_core.method_async(method_name=method_url, args=payload, files=files, method='post')

    async def send_audio(self, chat_id: int, audio, caption=None, duration: int = None, performer=None,
                         title: str = None, reply_to_message_id: int = None, reply_markup=None, parse_mode: int = None,
                         disable_notification=None, timeout: int = None, thumb=None):
        method_url = r'sendAudio'
        payload = {'chat_id': chat_id}
        files = None
        if not isinstance(audio, str):
            files = {'audio': audio}
        else:
            payload['audio'] = audio
        if caption:
            payload['caption'] = caption
        if duration:
            payload['duration'] = duration
        if performer:
            payload['performer'] = performer
        if title:
            payload['title'] = title
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
        if thumb:
            if not isinstance(thumb, str):
                files['thumb'] = thumb
            else:
                payload['thumb'] = thumb
        return await self._telegram_core.method_async(method_name=method_url, args=payload, files=files, method='post')

    async def send_data(self, chat_id: int, data, data_type: str, reply_to_message_id: int = None, reply_markup=None,
                        parse_mode: int = None, disable_notification=None, timeout: int = None, caption=None):
        method_url = self.get_method_by_type(data_type)
        payload = {'chat_id': chat_id}
        files = None
        if not isinstance(data, str):
            files = {data_type: data}
        else:
            payload[data_type] = data
        if reply_to_message_id:
            payload['reply_to_message_id'] = reply_to_message_id
        if reply_markup:
            payload['reply_markup'] = self._convert_markup(reply_markup)
        if parse_mode and data_type == 'document':
            payload['parse_mode'] = parse_mode
        if disable_notification is not None:
            payload['disable_notification'] = disable_notification
        if timeout:
            payload['connect-timeout'] = timeout
        if caption:
            payload['caption'] = caption
        return await self._telegram_core.method_async(method_name=method_url, args=payload, files=files, method='post')

    async def kick_chat_member(self, chat_id: int, user_id: int, until_date=None):
        method_url = 'kickChatMember'
        payload = {'chat_id': chat_id, 'user_id': user_id}
        if until_date:
            payload['until_date'] = until_date
        return await self._telegram_core.method_async(method_name=method_url, args=payload, method='post')

    async def unban_chat_member(self, chat_id: int, user_id: int):
        method_url = 'unbanChatMember'
        payload = {'chat_id': chat_id, 'user_id': user_id}
        return await self._telegram_core.method_async(method_name=method_url, args=payload, method='post')

    async def restrict_chat_member(self, chat_id: int, user_id: int, until_date=None,
                                   can_send_messages=None, can_send_media_messages=None,
                                   can_send_polls=None, can_send_other_messages=None,
                                   can_add_web_page_previews=None, can_change_info=None,
                                   can_invite_users=None, can_pin_messages=None):
        method_url = 'restrictChatMember'
        payload = {'chat_id': chat_id, 'user_id': user_id}
        if until_date is not None:
            payload['until_date'] = until_date
        if can_send_messages is not None:
            payload['can_send_messages'] = can_send_messages
        if can_send_media_messages is not None:
            payload['can_send_media_messages'] = can_send_media_messages
        if can_send_polls is not None:
            payload['can_send_polls'] = can_send_polls
        if can_send_other_messages is not None:
            payload['can_send_other_messages'] = can_send_other_messages
        if can_add_web_page_previews is not None:
            payload['can_add_web_page_previews'] = can_add_web_page_previews
        if can_change_info is not None:
            payload['can_change_info'] = can_change_info
        if can_invite_users is not None:
            payload['can_invite_users'] = can_invite_users
        if can_pin_messages is not None:
            payload['can_pin_messages'] = can_pin_messages
        return await self._telegram_core.method_async(method_name=method_url, args=payload, method='post')

    async def promote_chat_member(self, chat_id: int, user_id: int, can_change_info=None, can_post_messages=None,
                                  can_edit_messages=None, can_delete_messages=None, can_invite_users=None,
                                  can_restrict_members=None, can_pin_messages=None, can_promote_members=None):
        method_url = 'promoteChatMember'
        payload = {'chat_id': chat_id, 'user_id': user_id}
        if can_change_info is not None:
            payload['can_change_info'] = can_change_info
        if can_post_messages is not None:
            payload['can_post_messages'] = can_post_messages
        if can_edit_messages is not None:
            payload['can_edit_messages'] = can_edit_messages
        if can_delete_messages is not None:
            payload['can_delete_messages'] = can_delete_messages
        if can_invite_users is not None:
            payload['can_invite_users'] = can_invite_users
        if can_restrict_members is not None:
            payload['can_restrict_members'] = can_restrict_members
        if can_pin_messages is not None:
            payload['can_pin_messages'] = can_pin_messages
        if can_promote_members is not None:
            payload['can_promote_members'] = can_promote_members
        return await self._telegram_core.method_async(method_name=method_url, args=payload, method='post')

    async def set_chat_administrator_custom_title(self, chat_id: int, user_id: int, custom_title: str):
        method_url = 'setChatAdministratorCustomTitle'
        payload = {'chat_id': chat_id, 'user_id': user_id, 'custom_title': custom_title}
        return await self._telegram_core.method_async(method_name=method_url, args=payload, method='post')

    async def set_chat_permissions(self, chat_id: int, permissions):
        method_url = 'setChatPermissions'
        payload = {'chat_id': chat_id, 'permissions': permissions.to_json()}
        return await self._telegram_core.method_async(method_name=method_url, args=payload, method='post')

    def export_chat_invite_link(self, chat_id: int):
        method_url = 'exportChatInviteLink'
        payload = {'chat_id': chat_id}
        return await self._telegram_core.method_async(method_name=method_url, args=payload, method='post')

    async def set_chat_photo(self, chat_id: int, photo: any):
        method_url = 'setChatPhoto'
        payload = {'chat_id': chat_id}
        files = None
        if not isinstance(photo, str):
            files = {'photo': photo}
        else:
            payload['photo'] = photo
        return await self._telegram_core.method_async(method_name=method_url, args=payload, method='post', files=files)

    async def delete_chat_photo(self, chat_id: int):
        method_url = 'deleteChatPhoto'
        payload = {'chat_id': chat_id}
        return await self._telegram_core.method_async(method_name=method_url, args=payload, method='post')

    async def set_chat_title(self, chat_id: int, title: str):
        method_url = 'setChatTitle'
        payload = {'chat_id': chat_id, 'title': title}
        return await self._telegram_core.method_async(method_name=method_url, args=payload, method='post')

    async def set_my_commands(self, commands):
        method_url = r'setMyCommands'
        payload = {'commands': self._convert_list_json_serializable(commands)}
        return await self._telegram_core.method_async(method_name=method_url, args=payload, method='post')

    async def set_chat_description(self, chat_id: int, description: str):
        method_url = 'setChatDescription'
        payload = {'chat_id': chat_id, 'description': description}
        return await self._telegram_core.method_async(method_name=method_url, args=payload, method='post')

    async def pin_chat_message(self, chat_id: int, message_id: int, disable_notification=None):
        method_url = 'pinChatMessage'
        payload = {'chat_id': chat_id, 'message_id': message_id}
        if disable_notification is not None:
            payload['disable_notification'] = disable_notification
        return await self._telegram_core.method_async(method_name=method_url, args=payload, method='post')

    async def unpin_chat_message(self, chat_id: int):
        method_url = 'unpinChatMessage'
        payload = {'chat_id': chat_id}
        return await self._telegram_core.method_async(method_name=method_url, args=payload, method='post')

    async def edit_message_text(self, text: str, chat_id: int = None, message_id: int = None, reply_markup=None,
                                inline_message_id: int = None, parse_mode: int = None, disable_web_page_preview=None):
        method_url = r'editMessageText'
        payload = {'text': text}
        if chat_id:
            payload['chat_id'] = chat_id
        if message_id:
            payload['message_id'] = message_id
        if inline_message_id:
            payload['inline_message_id'] = inline_message_id
        if parse_mode:
            payload['parse_mode'] = parse_mode
        if disable_web_page_preview is not None:
            payload['disable_web_page_preview'] = disable_web_page_preview
        if reply_markup:
            payload['reply_markup'] = self._convert_markup(reply_markup)
        return await self._telegram_core.method_async(method_name=method_url, args=payload, method='post')

    async def edit_message_caption(self, caption, chat_id: int = None, message_id: int = None,
                                   inline_message_id: int = None,
                                   parse_mode: int = None, reply_markup=None):
        method_url = r'editMessageCaption'
        payload = {'caption': caption}
        if chat_id:
            payload['chat_id'] = chat_id
        if message_id:
            payload['message_id'] = message_id
        if inline_message_id:
            payload['inline_message_id'] = inline_message_id
        if parse_mode:
            payload['parse_mode'] = parse_mode
        if reply_markup:
            payload['reply_markup'] = self._convert_markup(reply_markup)
        return await self._telegram_core.method_async(method_name=method_url, args=payload, method='post')

    async def edit_message_media(self, media, chat_id: int = None, message_id: int = None,
                                 inline_message_id: int = None, reply_markup=None):
        method_url = r'editMessageMedia'
        media_json, file = self._convert_input_media(media)
        payload = {'media': media_json}
        if chat_id:
            payload['chat_id'] = chat_id
        if message_id:
            payload['message_id'] = message_id
        if inline_message_id:
            payload['inline_message_id'] = inline_message_id
        if reply_markup:
            payload['reply_markup'] = self._convert_markup(reply_markup)
            return await self._telegram_core.method_async(method_name=method_url, args=payload, files=file,
                                                          method='post' if file else 'get')

    async def edit_message_reply_markup(self, chat_id: int = None, message_id: int = None,
                                        inline_message_id: int = None, reply_markup=None):
        method_url = r'editMessageReplyMarkup'
        payload = {}
        if chat_id:
            payload['chat_id'] = chat_id
        if message_id:
            payload['message_id'] = message_id
        if inline_message_id:
            payload['inline_message_id'] = inline_message_id
        if reply_markup:
            payload['reply_markup'] = self._convert_markup(reply_markup)
        return await self._telegram_core.method_async(method_name=method_url, args=payload, method='post')

    async def delete_message(self, chat_id: int, message_id: int):
        method_url = r'deleteMessage'
        payload = {'chat_id': chat_id, 'message_id': message_id}
        return await self._telegram_core.method_async(method_name=method_url, args=payload, method='post')
