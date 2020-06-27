import warnings


class VkEvent:
    def __init__(self, vk_json: dict):
        self._vk_json = vk_json
        self.type: str = vk_json['type']
        self.obj: dict = vk_json['object']
        self.event_id: str = vk_json['event_id']
        self.group_event: int = vk_json['event_id']

    def is_typing_event(self):
        return self.type == 'message_typing_state'

    def to_msg_typing_event(self):
        if self.is_typing_event():
            return VkMsgTypingEvent(self._vk_json)
        else:
            warnings.warn("You tried to cast vk event to typing_event but it wasn't that event", RuntimeWarning)

    def is_message_new_event(self):
        return self.type == 'message_new'

    def to_message_new_event(self):
        if self.is_message_new_event():
            return _VkMsgNewEvent(self._vk_json)


class VkMsgTypingEvent(VkEvent):
    def __init__(self, vk_json: dict):
        super().__init__(vk_json)
        self.state: str = self.obj['state']
        self.from_id: int = self.obj['from_id']
        self.to_id: int = self.obj['to_id']


class _VkMsgNewEvent(VkEvent):
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

        if 'client_info' in self.obj:
            self.client_info_json: dict = self.obj['client_info']
            self.button_actions: list = self.client_info_json['button_actions']
            self.inline_keyboard: bool = self.client_info_json['inline_keyboard']
            self.lang_id: int = self.client_info_json['lang_id']

    def from_chat(self) -> bool:
        return self.msg_peer_id > int(2E9)

    def from_user(self) -> bool:
        return self.msg_peer_id < int(2E9)

    def to_chat_new_msg_event(self):
        if self.from_chat():
            return VkNewMsgChatEvent(self._vk_json)

    def to_user_new_msg_event(self):
        if self.from_chat():
            return VkNewMsgUserEvent(self._vk_json)


class VkNewMsgChatEvent(_VkMsgNewEvent):
    def __init__(self, vk_json: dict):
        super().__init__(vk_json)


class VkNewMsgUserEvent(_VkMsgNewEvent):
    def __init__(self, vk_json: dict):
        super().__init__(vk_json)