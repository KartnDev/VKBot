class ChannelInfo:
    def __init__(self, json_res: dict):
        self._json_data = json_res
        if 'status' in json_res:
            self.status = json_res['status']
        else:
            self.status = 'unknown'
        self.broadcaster_id = json_res['broadcaster_id']
        self.game_id = json_res['game_id']
        self.game_name = json_res['game_name']
        self.broadcaster_language = json_res['broadcaster_language']
        self.stream_title = json_res['title']
        self.broadcaster_name = json_res['broadcaster_name']
