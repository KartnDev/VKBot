import datetime


class TelegramChatEventSender:
    def __init__(self, telegram_json: dict):

        self.telegram_full_event = telegram_json

        self.update_id = telegram_json['update_id']
        self.message: dict = telegram_json['message']
        self.message_id: int = self.message['message_id']

        self.from_json: dict = self.message['from']

        self.from_id: int = self.from_json['id']
        self.is_bot: bool = self.from_json['is_bot']
        self.first_name_sender: str = self.from_json['first_name']
        self.last_name_sender: str = self.from_json['last_name']
        self.username_sender: str = self.from_json['username']
        self.language_code: str = self.from_json['language_code']

        self.chat_json: dict = self.message['chat']

        self.chat_id: int = self.chat_json['id']
        self.chat_first_name = self.chat_json['first_name']
        self.chat_last_name = self.chat_json['last_name']
        self.chat_username = self.chat_json['username']
        self.chat_first_name = self.chat_json['type']

        self.date_int32: int = self.message['date']
        self.date: datetime = datetime.timedelta(self.date_int32)

        self.text_msg = self.message['text']