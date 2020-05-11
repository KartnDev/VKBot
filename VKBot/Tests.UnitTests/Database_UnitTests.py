import unittest
import mysql.connector

from Src.Database.Connector import DbConnection


# noinspection DuplicatedCode
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

class UserWorkerTests:
    pass