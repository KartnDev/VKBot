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
