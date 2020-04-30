from enum import IntEnum
from collections.abc import Iterable
import warnings
import logging
import mysql.connector


class DbConnVersion(IntEnum):
    SYNC = 1
    ASYNC = 2
    COUPLE = 12


class DbSession:
    def __init__(self, host: str, database: str, username: str, password: str,
                 driver_ver: DbConnVersion = DbConnVersion.COUPLE):
        """
        Constructor that builds Sync and/or Async versions

        Args:
            host: name of host address  example : localhost
            database: name of the database that be connected
            username: name of Database user (root)
            password: ok that's real password
            driver_ver: defines the logic of the behavior of the driver:
                DbConnVersion.COUPLE = 12 as default and says that Connector should you 2 connections: sync and async
                DbConnVersion.ASYNC = only async, THROW ERROR IF YOU WILL USE "Sync" version methods
                DbConnVersion.SYNC = only sync,  THROW ERROR IF YOU WILL USE "Async" version methods

        Raises:
            Exception if driver cannot connect to the DB
        Warnings:
            RuntimeWarning if inside the class some method tried to connect while connection was opened

        """
        # sync version of driver
        self.driver_ver = driver_ver
        self._password = password
        self._username = username
        self._database = database
        self._host = host
        self._connection = mysql.connector.MySQLConnection()
        self._connect()

    def _connect(self):
        if self._connection.MySQLConnection.is_connected():
            try:
                self._connection.connect(host=self._host, database=self._database,
                                         user=self._username, password=self._password)
            except Exception as e:
                logging.critical(e)
                raise e
        else:
            warnings.warn("Already connected!", RuntimeWarning)

    def _base_select(self, select: str) -> Iterable:
        """

        Args:
            select: str type that will be executed in DataBase

        Returns:
            Iterable: if select was success
            NoneType: if select was failed
        Raises:
            Exception that
        """
        if not self._connection.is_connected():
            self._connect()

        records = None
        cursor = None
        try:
            cursor = self._connection.cursor()
            cursor.execute(select)
            records = cursor.fetchall()
        except Exception as e:
            logging.error(e)
            raise e
        finally:
            if self._connection.is_connected():
                self._connection.close()
                cursor.close()
        return records

    def select_all_table(self, table_name: str) -> Iterable:
        """
        Gives selected table (all columns)

        Args:
            table_name: string of Table that required

        Returns:
            Iterable: returns iterable top of objects with
            NoneType: if select was failed
        """
        return self._base_select("SELECT * FROM {0}".format(table_name))

    def select_top(self, table_name: str, top: int) -> Iterable:
        """
        Gives selected top with all columns

        Args:
            table_name: string of Table that required
            top: number of needed rows

        Returns:
            Iterable: returns iterable top of objects with all columns
            NoneType: if select was failed
        """
        return self._base_select("SELECT * FROM {0} LIMIT {1}".format(table_name, str(top)))

    def select_all_table(self, column_names: [str], table_name: str) -> Iterable:
        """
        Overload of select_all_table that's apply names of selected columns
        Gives selected table (all columns)

        Args:
            column_names: list of strings that contains names of table's columns
            table_name: string of Table that required

        Returns:
            Iterable: returns iterable top of objects with
            NoneType: if select was failed
        """
        return self._base_select("SELECT {0} FROM {1}".format(', '.join(name for name in column_names), table_name))

    def select_top(self, column_names: [str], table_name: str, top: int) -> Iterable:
        """
        Gives selected top with all columns

        Args:
            column_names: list of strings that contains names of table's columns
            table_name: string of Table that required
            top: number of needed rows

        Returns:
            Iterable: returns iterable top of objects with all columns
            NoneType: if select was failed
        """
        return self._base_select("SELECT {0} FROM {1} LIMIT {2}"
                                 .format(', '.join(name for name in column_names), table_name, str(top)))
