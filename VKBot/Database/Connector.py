import logging

import mysql as mysql

from Database.Models import BaseModel, OsuModel, CommandModel
from Database.Models.BaseModel import dbhandle, InternalError


class DbSession:
    """Метод(функция) инициализации класса
        в аргументы принимает модель таблицы с котоорой будет работать"""

    def __init__(self):
        self.connection = mysql.connector.connect(host='localhost',
                                             database='KartonDot',
                                             user='root',
                                             password='zxc123')





    def _base_select(self, select: str):
        """
        Args:
            select: str type that will be executed in DataBase

        Returns:
            object: if select was success
            NoneType: if select was failed
        """
        records = None
        cursor = None
        try:
            cursor = self.connection.cursor()
            cursor.execute(select)
            records = cursor.fetchall()
        except Exception as e:
            logging.error(e)
            raise e
        finally:
            if self.connection.is_connected():
                self.connection.close()
                cursor.close()
        return records
    """Метод загружает всю таблицу из бд"""

    def select_all_table(self):
        try:
            return self.model.select()
        except InternalError as ex:
            logging.error("exception were taken " + ex.with_traceback())
            raise ex

    def select_top(self):


    """Метод записи/добавления в таблицу данных
        :argument data : object то что заносится в базу данных (должно совпадать с типом стоблца)
        :argument column_name : object название столбца куда добавляешь"""

    def update(self, data, row_model):
        raise NotImplementedError

    """Метод записи в таблицу нового значения (строки)
    :argument row : BaseModel модель которую заносив в таблицу со всеми полями
    выкинет ошибку ArgumentError в несоответствии типов"""

    def insert(self, row_model):
        # TODO raise Error if attrs is incorrect
        row = row_model
        row.save()

    def delete(self, row_model):
        # TODO raise Error if attrs is incorrect
        row_model.delete_instance()