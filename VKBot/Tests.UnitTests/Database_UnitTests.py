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


