import logging
from collections import Iterable

from Src.Database.Connector import DbConnection, DbConnVersion
from Src.Database.Models import OsuModel


class OsuDbWorker:

    def __init__(self):
        self.db = DbConnection('localhost', 'KartonBot', 'root', 'zxc123', 3306, DbConnVersion.SYNC)
        self.table_name = 'osu'

    def select_all(self) -> Iterable:
        data = self.db.select_all_table(self.table_name, ['vk_id', 'nickname', 'mode'])
        items = []
        for item in data:
            items.append({
                'vk_id': item[0],
                'nickname': item[1],
                'mode': item[2]})

        return items

    def select_one(self, osu_vk_id: int) -> object:
        return self.db.select_where(self.table_name, {'vk_id': osu_vk_id})

    def insert(self, osu_vk_id: int, osu_nickname: str, mode: int = 1):
        return self.db.insert_into(self.table_name, {'vk_id': osu_vk_id,
                                                     'nickname': osu_nickname,
                                                     'mode': mode})

    def delete(self, osu_vk_id: int) -> bool:
        return self.db.delete_where(self.table_name, {'vk_id': osu_vk_id})

    def update(self, vk_id, nickname: str = None, mode: int = None) -> bool:
        args = locals()
        if any(args.values()) is not None:
            dict_of_updates = {}
            if nickname is not None:
                dict_of_updates.update({'nickname': nickname})
            if mode is not None:
                dict_of_updates.update({'mode': mode})

            return self.db.update_where(self.table_name, {'vk_id': vk_id}, dict_of_updates)
        else:
            logging.warning('taken zero params and cannot be any update..')
            return False

