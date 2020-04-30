import asyncio
from enum import IntEnum
from collections.abc import Iterable
import warnings
import logging

import aiomysql
import mysql.connector


class DbConnVersion(IntEnum):
    SYNC = 1
    ASYNC = 2
    COUPLE = 12


class DbSession:
    def __init__(self, host: str, database: str, username: str, password: str, port: int,
                 driver_ver: DbConnVersion = DbConnVersion.COUPLE):
        """
        Constructor that builds Sync and/or Async versions

        Args:
            port: int port of mysql instance
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
        self._port = port
        self.driver_ver = driver_ver
        self._password = password
        self._username = username
        self._database = database
        self._host = host
        self._connection = mysql.connector.MySQLConnection()
        self._connect_to_sync()

    def _connect_to_sync(self):
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
            Exception that was taken by critical runtime error
        """
        if not self._connection.is_connected():
            self._connect_to_sync()

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

    async def _connect_to_async(self, loop):
        _async_conn = None
        try:
            _async_conn = await aiomysql.create_pool(host=self._host, port=3306,
                                                     user=self._username, password=self._password,
                                                     db=self._database, loop=loop)
            return _async_conn
        except Exception as e:
            logging.critical(e)
            raise e

    async def _base_select_async(self, select: str, loop) -> Iterable:
        """
            asynchronous version of protected method _base_select
        Args:
            loop (asyncio Async POOL): pool of asyncio io that can be got by call asyncio.get_pool
            select: str type that will be executed in DataBase

        Returns:
            Iterable: if select was success
            NoneType: if select was failed
        Raises:
            Exception that
        """
        _aw_pool_result = None
        _as_pool = await self._connect_to_async(loop)
        async with _as_pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(select)
                _aw_pool_result = await cur.fetchall()
        _as_pool.close()
        await _as_pool.wait_closed()
        return _aw_pool_result

    async def select_all_table_async(self, table_name: str, loop) -> Iterable:
        """
        asynchronous version of protected method select_all_table
        Gives selected table (all columns)

        Args:
            table_name: string of Table that required
            loop (asyncio Async POOL): pool of asyncio io that can be got by call asyncio.get_pool
        Returns:
            Iterable: returns iterable top of objects with
            NoneType: if select was failed
        """
        return await self._base_select_async("SELECT * FROM {0}".format(table_name), loop)
