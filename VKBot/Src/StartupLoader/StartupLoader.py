import json
import logging
import pathlib

from Src.Database.CommandDbWorker import CommandDbWorker
from Src.Database.UserDbWorker import UserDbWorker


class StartupLoader:
    def __init__(self, config_name: str):
        logging.basicConfig(filename="logBook.log", level=logging.INFO)
        with open(str(pathlib.Path().absolute()) + '/StartupLoader/' + config_name) as json_file:
            self.data = json.load(json_file)

    def load_users_list(self) -> list:
        user_worker = UserDbWorker()
        return user_worker.select_all()

    def load_commands_list(self) -> list:
        command_worker = CommandDbWorker()
        return command_worker.select_all()

    def get_admin_id(self) -> int:
        return self.data['bot_admin']

    def get_vk_token(self) -> str:
        return self.data['token']

    def get_osu_token(self) -> str:
        return self.data['osu_token']