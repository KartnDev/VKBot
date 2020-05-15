import unittest
from collections import Sized
from typing import Iterable

import mysql.connector

from Src.Database.Connector import DbConnection


# noinspection DuplicatedCode
from Src.Database.UserDbWorker import UserDbWorker


class ConnectorDataBaseTest(unittest.TestCase):

    def test_select_all_table(self):
        _database = DbConnection('localhost', 'KartonBot', 'root', 'zxc123', 3306)
        query_connector = _database.select_all_table(table_name='users')

        _driver = mysql.connector.connect(host='localhost', database='mysql', user='root', password='zxc123')
        _cur = _driver.cursor()
        _cur.execute("select * from Kartonbot.users")
        query_driver = _cur.fetchall()
        for dr_item, conn_item in zip(query_driver, query_connector):
            print(dr_item, " | ", conn_item)
            self.assertEqual(dr_item, conn_item)

    def test_select_top(self):
        _database = DbConnection('localhost', 'KartonBot', 'root', 'zxc123', 3306)
        query_connector = _database.select_top(table_name='users', top=2)

        _driver = mysql.connector.connect(host='localhost', database='mysql', user='root', password='zxc123')
        _cur = _driver.cursor()
        _cur.execute("select * from Kartonbot.users limit 2")
        query_driver = _cur.fetchall()
        for dr_item, conn_item in zip(query_driver, query_connector):
            print(dr_item, " | ", conn_item)
            self.assertEqual(dr_item, conn_item)

    def test_select_all_columns(self):
        _database = DbConnection('localhost', 'KartonBot', 'root', 'zxc123', 3306)
        query_connector = _database.select_all_table(table_name='users', column_names=['id', 'vk_id'])
        _driver = mysql.connector.connect(host='localhost', database='mysql', user='root', password='zxc123')
        _cur = _driver.cursor()
        _cur.execute("select id, vk_id from Kartonbot.users limit 2")
        query_driver = _cur.fetchall()
        for dr_item, conn_item in zip(query_driver, query_connector):
            print(dr_item, " | ", conn_item)
            self.assertEqual(dr_item, conn_item)

    def test_select_top_columns(self):
        _database = DbConnection('localhost', 'KartonBot', 'root', 'zxc123', 3306)
        query_connector = _database.select_top(table_name='users', top=2, column_names=['association', 'id'])

        _driver = mysql.connector.connect(host='localhost', database='mysql', user='root', password='zxc123')
        _cur = _driver.cursor()
        _cur.execute("select association, id from Kartonbot.users limit 2")
        query_driver = _cur.fetchall()
        for dr_item, conn_item in zip(query_driver, query_connector):
            print(dr_item, " | ", conn_item)
            self.assertEqual(dr_item, conn_item)

    def test_select_where(self):
        _database = DbConnection('localhost', 'KartonBot', 'root', 'zxc123', 3306)
        query_connector = _database.select_where(table_name='users', where_condition={'id': 1})

        _driver = mysql.connector.connect(host='localhost', database='mysql', user='root', password='zxc123')
        _cur = _driver.cursor()
        _cur.execute("select * from Kartonbot.users where id=1")
        query_driver = _cur.fetchall()
        for dr_item, conn_item in zip(query_driver, query_connector):
            print(dr_item, " | ", conn_item)
            self.assertEqual(dr_item, conn_item)

        query_connector = _database.select_where(table_name='users', where_condition={'id': 1,
                                                                                      'association': 'Дима'})

        _cur.execute("select * from Kartonbot.users where id=1 AND association='Дима'")
        query_driver = _cur.fetchall()
        for dr_item, conn_item in zip(query_driver, query_connector):
            print(dr_item, " | ", conn_item)
            self.assertEqual(dr_item, conn_item)

    def test_insert_into(self):
        _database = DbConnection('localhost', 'KartonBot', 'root', 'zxc123', 3306)
        query_connector = _database.insert_into('users', {'association': 'asc',
                                                          'access_level': 1,
                                                          'vk_id': 13372281,
                                                          'lvl_exp': 1.0})

        _driver = mysql.connector.connect(host='localhost', database='mysql', user='root', password='zxc123')
        _cur = _driver.cursor()
        _cur.execute("select * from Kartonbot.users where id=4")
        query_driver = _cur.fetchall()
        for dr_item, first_item in zip(query_driver, [(100, 1, 13372281, 'asc', 1.0)]):
            print(dr_item, " | ", first_item)
            self.assertEqual(dr_item, first_item)

    def test_delete_where(self):
        _database = DbConnection('localhost', 'KartonBot', 'root', 'zxc123', 3306)
        query_connector = _database.select_all_table('users')
        # TODO WTF Sized != Iterable
        _last_len = len(query_connector)

        _database.delete_where('users', {'id': 5})

        self.assertEqual(len(_database.select_all_table('users')), _last_len - 1)

    def test_update_where(self):
        _database = DbConnection('localhost', 'KartonBot', 'root', 'zxc123', 3306)
        _first = _database.select_where('users', {'id': 1})
        _database.update_where('users', {'id': 1}, {'association': 'дима'})
        _last = _database.select_where('users', {'id': 1})
        print(_first, " != ", _last)
        self.assertNotEqual(_first, _last)
        self.assertEqual(_last, [(1, 1, 376359640, 'дима', 1000.9)])

    def test_update_where_multi(self):
        _database = DbConnection('localhost', 'KartonBot', 'root', 'zxc123', 3306)
        _first = _database.select_where('users', {'id': 1, 'vk_id': 376359640})
        _database.update_where('users', {'id': 1}, {'association': 'dima', 'lvl_exp': 0.9})
        _last = _database.select_where('users', {'id': 1, 'vk_id': 376359640})
        print(_first, " != ", _last)
        self.assertNotEqual(_first, _last)
        self.assertEqual(_last, [(1, 1, 376359640, 'dima', 0.9)])


class UserDbWorkerTest(unittest.TestCase):
    def test_select_all(self):
        users_worker = UserDbWorker()
        data_from_worker = users_worker.select_all()

        _database = DbConnection('localhost', 'KartonBot', 'root', 'zxc123', 3306)
        _pure_data = _database.select_all_table('users', ['access_level', 'vk_id', 'association', 'lvl_exp'])
        for taken_item, action in zip(_pure_data, data_from_worker):
            print(taken_item, " | ", action)
            self.assertEqual(taken_item[0], action['access_level'])
            self.assertEqual(taken_item[1], action['vk_id'])
            self.assertEqual(taken_item[2], action['association'])
            self.assertEqual(taken_item[3], action['lvl_exp'])

    def test_insert(self):
        _database = DbConnection('localhost', 'KartonBot', 'root', 'zxc123', 3306)

        users_worker = UserDbWorker()
        users_worker.insert(23, 1234567, 'mobyDickDuck', 1000.1)

        _new_data = _database.select_where('users', {'vk_id': 1234567})
        print(_new_data[0])
        self.assertEqual(_new_data[0][1], 23)
        self.assertEqual(_new_data[0][2], 1234567)
        self.assertEqual(_new_data[0][3], 'mobyDickDuck')
        self.assertEqual(_new_data[0][4], 1000.1)

    def test_delete(self):
        users_worker = UserDbWorker()
        _old_list = users_worker.select_all()

        self.assertTrue([item for item in _old_list if item['vk_id'] == 22813311] != [])
        self.assertTrue(users_worker.delete(22813311))
        _new_list = users_worker.select_all()

        for _old, _new in zip(_old_list, _new_list):
            print(_old, ' | ', _new)
        self.assertEqual(len(_old_list), len(_new_list) + 1)
        self.assertEqual([item for item in _new_list if item['vk_id'] == 22813311], [])

    def test_update(self):
        _database = DbConnection('localhost', 'KartonBot', 'root', 'zxc123', 3306)
        _old_row = _database.select_where('users', {'vk_id': 376359640})[0]

        self.assertNotEqual(_old_row[3], 'дима')
        self.assertEqual(_old_row[3], 'dima')

        users_worker = UserDbWorker()
        users_worker.update(376359640, association='дима')

        _new_row = _database.select_where('users', {'vk_id': 376359640})[0]

        self.assertEqual(_new_row[3], 'дима')



class CommandDbWorkerTest(unittest.TestCase):
    def test_select_all(self):
        pass

    def test_insert(self):
        pass

    def test_delete(self):
        pass

    def test_update(self):
        pass


class OsuDbWorkerTest(unittest.TestCase):
    def test_select_all(self):
        pass

    def test_insert(self):
        pass

    def test_delete(self):
        pass

    def test_update(self):
        pass