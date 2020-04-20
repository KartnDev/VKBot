class ChatEventSender:
    def __init__(self, chat_id: int, user_sender_id: int, event: dict(),):
        """
        :param chat_id: int > 0
        :param user_sender_id: vk_id > 0
        :param event: dictionary like
        {
            "message": "some_message" or None,
            "attachment": "attachment" or None
            etc
        }
        """

        self.chat_id = chat_id
        self.user_id = user_sender_id
        self.event = event


class UserEventSender:
    def __init__(self, user_sender_id: int, event: dict()):
        """
        :param user_sender_id: vk_id > 0
        :param event: dictionary like
        {
            "message": "some_message" or None,
            "attachment": "attachment" or None
            etc
        }
        """

        self.user_id = user_sender_id
        self.event = event