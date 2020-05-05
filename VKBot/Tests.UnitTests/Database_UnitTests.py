import unittest
import mysql.connector


class ConnectorDataBaseTest(unittest.TestCase):

    def test_select_all_table(self):
        from Src.Database.Connector import DbConnection
        _database = DbConnection('localhost', 'KartonBot', 'root', 'zxc123', 3306)
        query_connector = _database.select_all_table(table_name='users')

        _driver = mysql.connector.connect(host='localhost', database='mysql', user='root', password='zxc123')
        _cur = _driver.cursor()
        _cur.execute("select * from Kartonbot.users")
        query_driver = _cur.fetchall()
        for dr_item, conn_item in zip(query_driver, query_connector):
            self.assertEqual(dr_item, conn_item)

    def test_select_top(self):
        from Src.Database.Connector import DbConnection
        _database = DbConnection('localhost', 'KartonBot', 'root', 'zxc123', 3306)
        query_connector = _database.select_top(table_name='users', top=2)

        _driver = mysql.connector.connect(host='localhost', database='mysql', user='root', password='zxc123')
        _cur = _driver.cursor()
        _cur.execute("select * from Kartonbot.users limit 2")
        query_driver = _cur.fetchall()
        for dr_item, conn_item in zip(query_driver, query_connector):
            self.assertEqual(dr_item, conn_item)

if __name__ == '__main__':
    unittest.main(ConnectorDataBaseTest)