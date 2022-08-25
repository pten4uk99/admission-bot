import os
import sqlite3
from sqlite3 import Connection

from config import BASE_DIR, DATABASE
from db.base.field_types import DBFieldTypes


class Backend:
    """
    Интерфейс для реализации подключения к выбранной базе данных.

    При наследовании:
    self.get_db_name - возвращает имя базы данных из словаря DATABASE, определенного в настройках.
    self.connect() - непосредственное подключение к БД. Возвращает объект подключения.
    """
    types: DBFieldTypes = None

    def __init__(self):
        self.db_module = self.get_db_module()
        self.db_name = self.get_db_name()

    def get_db_name(self):
        assert isinstance(DATABASE, dict), 'DATABASE переменная должна быть словарем'

        db_name = DATABASE.get('NAME', None)
        assert db_name is not None, 'DATABASE переменная неверно сконфигурирована'
        return db_name

    def get_db_module(self):
        """ Возвращает модуль, который предоставляет интерфейс для взаимодействия с выбранной БД """

        raise NotImplementedError()

    def connect(self):
        """ Возвращает подключение к БД """

        raise NotImplementedError()


class SQLiteBackend(Backend):
    types = DBFieldTypes(
        STRING='TEXT',
        NUMBER='INTEGER',
        BYTES='BLOB',
        FLOAT='REAL',
        BOOLEAN='BOOLEAN'
    )

    def get_db_module(self):
        return sqlite3

    def _get_db_folder(self):
        return 'db'

    def _get_path_to_db(self) -> str:
        db_name = self.get_db_name()
        db_folder = self._get_db_folder()

        relative_path = os.path.join(db_folder, db_name)
        absolute_path = os.path.join(BASE_DIR, relative_path)
        return absolute_path + '.db'

    def connect(self) -> Connection:
        return self.db_module.connect(self._get_path_to_db())


if __name__ == '__main__':
    backend = SQLiteBackend()
    connection = backend.connect()
    cursor = connection.cursor()

    cursor.execute("""
    INSERT INTO student (chat_id) VALUES (12)
    """)

