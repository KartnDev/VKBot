import warnings


class ChatEventSender:
    def __init__(self, chat_id: int, user_sender_id: int, msg_event: dict, all_data_event: dict = None):
        """
        :param chat_id: int > 0
        :param user_sender_id: vk_id > 0
        :param msg_event: dictionary like
        {
            "message": "some_message" or None,
            "attachment": "attachment" or None
            etc
        }
        """
        self.chat_id = chat_id
        self.user_id = user_sender_id
        self.event = msg_event
        if all_data_event is not None:
            self.all_data_event = all_data_event


class UserEventSender:
    def __init__(self, user_sender_id: int, msg_event: dict, all_data_event: dict = None):
        """
        :param user_sender_id: vk_id > 0
        :param msg_event: dictionary like
        {
            "message": "some_message" or None,
            "attachment": "attachment" or None
            etc
        }
        """

        self.user_id = user_sender_id
        self.event = msg_event
        if all_data_event is not None:
            self.all_data_event = all_data_event


#   TODO reformat it with many data

class VkEventSender:
    def __init__(self, all_data_event: dict):
        self.all_data_event = all_data_event


class VkEvent:
    def __init__(self, vk_json: dict):
        self._vk_json = vk_json
        self.type: str = vk_json['type']
        self.obj: dict = vk_json['object']
        self.event_id: str = vk_json['event_id']
        self.group_event: int = vk_json['event_id']

    def is_typing_event(self):
        return self.type == 'message_typing_state'

    def to_msg_typing_event(self) -> VkMsgTypingEvent:
        if self.is_typing_event():
            return VkMsgTypingEvent(self._vk_json)
        else:
            warnings.warn("You tried to cast vk event to typing_event but it wasn't that event", RuntimeWarning)

    def is_message_new_event(self):
        return self.type == 'message_new'

    def to_message_new_event(self):


class VkMsgTypingEvent(VkEvent):
    def __init__(self, vk_json: dict):
        super().__init__(vk_json)
        self.state: str = self.obj['state']
        self.from_id: int = self.obj['from_id']
        self.to_id: int = self.obj['to_id']

class VkMsgNewEvent(VkEvent):
    def __init__(self, vk_json: dict):
        super().__init__(vk_json)
        self.message_json: dict = self.obj['message']
        self.msg_date: int = self.message_json['date']
        self.msg_from: int = self.message_json['from_id']
        self.msg_id: int = self.message_json['id']
        self.msg_out: int = self.message_json['out']
        self.msg_peer_id: int = self.message_json['peer_id']
        self.msg_text: str = self.message_json['text']
        self.msg_conversation_message_id: int = self.message_json['conversation_message_id']
        self.msg_fwd_message: list = self.message_json['fwd_messages']
        self.msg_important: bool = self.message_json['important']
        self.msg_random_id: int = self.message_json['random_id']
        self.msg_attachments: list = self.message_json['attachments']
        self.msg_is_hidden: bool = self.message_json['is_hidden']