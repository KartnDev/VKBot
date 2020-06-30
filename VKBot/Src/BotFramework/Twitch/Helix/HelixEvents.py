import datetime


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


class StreamInfo:
    def __init__(self, json_res: dict):
        self._json_res = json_res
        self.broadcaster_language: str = json_res['broadcaster_language']
        self.streamer_nickname: str = json_res['display_name']
        self.game_id: int = int(json_res['game_id'])
        self.id: int = int(json_res['id'])
        self.is_life: bool = json_res['is_live']
        self.tag_guid_ids: str = json_res['tag_ids']
        self.thumbnail_url: str = json_res['thumbnail_url']
        self.stream_title: str = json_res['title']
        self.stream_started_at: str = json_res['started_at']

    def __str__(self):
        return """
        streamer_nickname: {0}
        is_streaming: {1}
        stream_title: {2}
        broadcaster_language: {3}
        """.format(self.streamer_nickname, self.is_life, self.stream_title, self.broadcaster_language)

    def get_started_at_as_datetime(self) -> datetime.datetime:
        return datetime.datetime.strptime(self.stream_started_at, "%Y-%m-%dT%H:%M:%SZ")