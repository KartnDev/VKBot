import unittest
import mysql.connector
from Src.Database.CommandDbWorker import CommandDbWorker
from Src.Database.Connector import DbConnection
from Src.Database.OsuDbWorker import OsuDbWorker
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

    def test_contains(self):
        users_worker = UserDbWorker()
        #users_worker.insert(10, 98712364, 'html', 7777)
        self.assertTrue(users_worker.contains(98712364))
        self.assertFalse(users_worker.contains(213))



class CommandDbWorkerTest(unittest.TestCase):
    def test_select_all(self):
        command_worker = CommandDbWorker()
        data_from_worker = command_worker.select_all()

        _database = DbConnection('localhost', 'KartonBot', 'root', 'zxc123', 3306)
        _pure_data = _database.select_all_table('categories', ['access_level', 'name', 'value', 'attachment'])
        for taken_item, action in zip(_pure_data, data_from_worker):
            print(taken_item, " | ", action)
            self.assertEqual(taken_item[0], action['access_level'])
            self.assertEqual(taken_item[1], action['name'])
            self.assertEqual(taken_item[2], action['value'])
            self.assertEqual(taken_item[3], action['attachment'])

    def test_insert(self):
        command_worker = CommandDbWorker()
        _database = DbConnection('localhost', 'KartonBot', 'root', 'zxc123', 3306)

        command_worker.insert(23, '12345671', 'mobysafdsasffdsafsdfdsafDickDuck', '1000.1')

        _new_data = _database.select_where('categories', {'name': '12345671'})
        print(_new_data[0])
        self.assertEqual(_new_data[0][1], 23)
        self.assertEqual(_new_data[0][2], '12345671')
        self.assertEqual(_new_data[0][3], 'mobysafdsasffdsafsdfdsafDickDuck')
        self.assertEqual(_new_data[0][4], '1000.1')

    def test_delete(self):
        command_worker = CommandDbWorker()
        _old_c_list = command_worker.select_all()

        self.assertTrue([item for item in _old_c_list if item['name'] == 'QQ'] != [])
        self.assertTrue(command_worker.delete('QQ'))
        _new_c_list = command_worker.select_all()

        for _old, _new in zip(_old_c_list, _new_c_list):
            print(_old, ' | ', _new)
        self.assertEqual(len(_old_c_list), len(_new_c_list) + 1)
        self.assertEqual([item for item in _new_c_list if item['name'] == 'QQ'], [])

    def test_update(self):
        _database = DbConnection('localhost', 'KartonBot', 'root', 'zxc123', 3306)
        _old_c_row = _database.select_where('categories', {'name': '1000'})[0]

        self.assertNotEqual(_old_c_row[3], '!hi')
        self.assertEqual(_old_c_row[3], 'ihjpds')

        command_worker = CommandDbWorker()
        command_worker.update('1000', value='!hi')

        _new_row = _database.select_where('categories', {'name': '1000'})[0]

        self.assertEqual(_new_row[3], '!hi')


class OsuDbWorkerTest(unittest.TestCase):
    def test_select_all(self):
        _osu_wr = OsuDbWorker()
        data_from_worker = _osu_wr.select_all()

        _database = DbConnection('localhost', 'KartonBot', 'root', 'zxc123', 3306)
        _pure_data = _database.select_all_table('osu', ['vk_id', 'nickname', 'mode'])
        for taken_item, action in zip(_pure_data, data_from_worker):
            print(taken_item, " | ", action)
            self.assertEqual(taken_item[0], action['vk_id'])
            self.assertEqual(taken_item[1], action['nickname'])
            self.assertEqual(taken_item[2], action['mode'])

    def test_insert(self):
        _osu_wr = OsuDbWorker()
        _database = DbConnection('localhost', 'KartonBot', 'root', 'zxc123', 3306)

        _osu_wr.insert(23312321, 'negative', 1)

        _new_data = _database.select_where('osu', {'vk_id': 23312321})
        print(_new_data[0])
        self.assertEqual(_new_data[0][1], 23312321)
        self.assertEqual(_new_data[0][2], 'negative')
        self.assertEqual(_new_data[0][3], 1)

    def test_delete(self):
        _osu_wr = OsuDbWorker()
        _old_o_list = _osu_wr.select_all()

        self.assertTrue([item for item in _old_o_list if item['vk_id'] == 123221] != [])
        self.assertTrue(_osu_wr.delete(123221))
        _new_c_list = _osu_wr.select_all()

        for _old, _new in zip(_old_o_list, _new_c_list):
            print(_old, ' | ', _new)
        self.assertEqual(len(_old_o_list), len(_new_c_list) + 1)
        self.assertEqual([item for item in _new_c_list if item['vk_id'] == 123221], [])

    def test_update(self):
        _database = DbConnection('localhost', 'KartonBot', 'root', 'zxc123', 3306)
        _old_o_row = _database.select_where('osu', {'vk_id': 12312321})[0]

        self.assertNotEqual(_old_o_row[2], 'pupa')
        self.assertEqual(_old_o_row[2], 'biba')

        _osu_wr = OsuDbWorker()
        _osu_wr.update(12312321, nickname='pupa')

        _new_row = _database.select_where('osu', {'vk_id': 12312321})[0]

        self.assertEqual(_new_row[2], 'pupa')

    def test_select_one(self):
        _database = DbConnection('localhost', 'KartonBot', 'root', 'zxc123', 3306)
        _old_o_row = _database.select_where('osu', {'vk_id': 12312321})[0]

        _osu_wr = OsuDbWorker()
        _new_row = _osu_wr.select_one('12312321')[0]

        self.assertEqual(_old_o_row, _new_row)
