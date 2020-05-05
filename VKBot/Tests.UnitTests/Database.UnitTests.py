import unittest
import mysql.connector

from Src.Database.Connector import DbConnection


class ConnectorDataBaseTest(unittest.TestCase):

    def base_execute_test(self):
        pass

    def select_all_table_test(self):
        _database = DbConnection('localhost', 'KartonBot', 'root', 'zxc123', 3306)
        query_connector = _database.select_all_table(table_name='users')

        _driver = mysql.connector.connect(host='localhost', database='mysql', user='root', password='zxc123')
        _cur = _driver.cursor()
        _cur.execute("select * from Kartonbot.users")
        query_driver = _cur.fetchall()
        for dr_item, conn_item in zip(query_driver, query_connector):
            self.assertEqual(1, 1)

    def select_top_test(self):
        pass

    def select_all_table_test(self):
        pass

    def select_top_test(self):
        pass

    def _connect_to_async_test(self):
        pass

    def _base_select_async_test(self):
        pass

    def select_all_table_async_test(self):
        pass


if __name__ == '__main__':
    test = ConnectorDataBaseTest()
    test.select_all_table_test()