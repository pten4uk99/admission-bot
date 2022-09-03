from sqlite3 import Cursor, Connection, Row
from typing import Type, TypeVar

from db.base.backends import Backend
from db.base.fields import Field
from db.base.model import Model
from db.base.query import GetQuery, CreateTableQuery, InsertQuery, UpdateQuery
from db.base.utils import camel_to_snake

QueryClass = TypeVar('QueryClass')


class SQLException(Exception):
    pass


class SQLFactory:
    def __init__(self, instance_class: Type[Model], db_backend: Backend, connection):
        self.instance_class = instance_class
        self.db_backend = db_backend
        self.connection: Connection = connection

        # Эта строчка означает, что методы fetch будут возвращать словари с данными, а не кортежи
        self.connection.row_factory = Row
        self.cursor: Cursor = connection.cursor()

        assert issubclass(self.instance_class, Model), (
            '{} должен быть типом {}'.format(self.instance_class, Model)
        )

        self.table_name: str = camel_to_snake(self.instance_class.__name__)
        self.table_fields: list[Field] = self.instance_class.get_fields()

        self.raw_sql: str = ''
        self.__instance = None

    @property
    def instance(self):
        return self.__instance

    @instance.setter
    def instance(self, value):
        assert isinstance(value, self.instance_class), '"instance" должен быть типом {}'.format(self.instance_class)
        self.__instance = value

    @property
    def raw_sql(self):
        return self.__raw_sql

    @raw_sql.setter
    def raw_sql(self, value):
        assert isinstance(value, str), '"raw_sql" атрибут должен быть строкой'
        self.__raw_sql = value

    def clear_query(self) -> None:
        """ Очищает строку запроса SQL """

        self.raw_sql = ''

    def _fetch_one(self, fetched: list[Row]):
        """ Срабатывает при использовании self.perform_fetch(), если не передан параметр many """

        assert len(fetched) < 2, 'Запрос возвратил больше одного объекта'
        if len(fetched) == 1:
            row = fetched[0]
            return self.instance_class(**row)

    def _fetch_many(self, fetched: list[Row]):
        """ Срабатывает при использовании self.perform_fetch(), если передан параметр many=True """

        result = []
        for elem in fetched:
            result.append(self.instance_class(**elem))
        return result

    def perform_fetch(self, many: bool = False):
        assert 'SELECT' in self.raw_sql, "Вызвать метод 'perform_fetch' можно только с SELECT запросом"
        self.cursor.execute(self.raw_sql)

        fetch: list[Row] = self.cursor.fetchall()
        self.clear_query()

        if not many:
            return self._fetch_one(fetched=fetch)
        else:
            return self._fetch_many(fetched=fetch)

    def perform_update(self, commit: bool = True):
        """ Выполняет SQL запрос, вносящий какие либо изменения в БД, составленный в self.raw_sql """

        assert 'CREATE' in self.raw_sql or \
               'UPDATE' in self.raw_sql or \
               'DELETE' in self.raw_sql or \
               'INSERT' in self.raw_sql, (
            'Вызвать метод "perform_update" можно только с запросом, вносящим изменения в БД'
        )

        self.cursor.execute(self.raw_sql)
        self.clear_query()

        if commit:
            self.connection.commit()

    def _init_query_class(self, query_class: Type[QueryClass]) -> QueryClass:
        return query_class(
            instance=self.instance_class,
            table_name=self.table_name,
            table_fields=self.table_fields
        )

    def create_table(self) -> None:
        """
        Создает SQL запрос для создания таблицы на основе текущей модели в БД
        и записывает его в self.raw_sql
        """

        query_ = self._init_query_class(CreateTableQuery)
        self.raw_sql = query_.get_sql()

    def create(self, **kwargs) -> None:
        """
        Создает запрос для создания объекта текущей модели в БД
        и записывает его в self.raw_sql
        """

        query_ = self._init_query_class(InsertQuery)
        query_.insert_values(**kwargs)
        self.raw_sql = query_.get_sql()

    def get(self, all_tables: bool = False, **kwargs) -> None:
        assert all_tables or kwargs, 'Не переданы параметры фильтрации'

        query_ = self._init_query_class(GetQuery)
        if not all_tables:
            query_.where(**kwargs)
        self.raw_sql = query_.get_sql()

    def update(self, **kwargs):
        """
        Создает запрос для обновления данных объекта текущей модели в БД
        и записывает его в self.raw_sql
        """

        assert self.instance is not None, 'Необходимо определить атрибут "instance" прежде чем вызывать метод update()'
        query_ = self._init_query_class(UpdateQuery)
        query_.where(**kwargs)
        query_.bind_obj(self.instance)
        self.raw_sql = query_.get_sql()


if __name__ == '__main__':
    pass
