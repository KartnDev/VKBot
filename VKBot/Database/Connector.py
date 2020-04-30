import logging



from Database.Models import BaseModel, OsuModel, CommandModel
from Database.Models.BaseModel import dbhandle, InternalError


class DbSession:
    """Метод(функция) инициализации класса
        в аргументы принимает модель таблицы с котоорой будет работать"""

    def __init__(self):
        # sync version of driver
        self.connection = mysql.connector.connect(host='localhost',
                                             database='KartonDot',
                                             user='root',
                                             password='zxc123')

    def _base_select(self, select: str) -> object:
        """

        Args:
            select: str type that will be executed in DataBase

        Returns:
            object: if select was success
            NoneType: if select was failed
        Raises:
            Exception that
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

    def select_all_table(self, table_name: str) -> object:
        """
        Gives selected table (all columns)

        Args:
            table_name: string of Table that required

        Returns:
            object: returns iterable top of objects with
        """
        return self._base_select("SELECT * FROM {0}".format(table_name))

    def select_top(self, table_name: str, top: int) -> object:
        """
        Gives selected top with all columns

        Args:
            table_name: string of Table that required
            top: number of needed rows

        Returns:
            object: returns iterable top of objects with all columns
        """
        return self._base_select("SELECT * FROM {0} LIMIT {1}".format(table_name, str(top)))

    def select_all_table(self, column_names: [str], table_name: str) -> object:
        """
        Gives selected table (all columns)

        Args:
            column_names: list of strings that contains names of table's columns
            table_name: string of Table that required

        Returns:
            object: returns iterable top of objects with
        """
        return self._base_select("SELECT {0} FROM {1}".format(', '.join(name for name in column_names), table_name))

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