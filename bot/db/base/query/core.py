from typing import Type

from db.base.fields import Field
from db.base.model import Model
from db.base.query.base import Query
from db.base.query.mixins import WhereMixin


class CreateTableQuery(Query):
    def get_table_fields_rows(self) -> str:
        """ Возвращает строку с готовой SQL строкой для каждого поля модели """

        assert self.table_fields, "Модель {} должна содержать как минимум одно поле".format(self.instance)

        rows = []
        foreign_keys = []
        for field in self.table_fields:
            rows.append(field.to_sql())
            if field.foreign_key:
                foreign_keys.append(field.get_foreign_key_sql())

        result = rows + foreign_keys
        return ', '.join(result)

    def get_sql(self) -> str:
        fields = self.get_table_fields_rows()
        return f'CREATE TABLE IF NOT EXISTS {self.table_name}({fields});'


class InsertQuery(Query):
    def __init__(self, instance: Type[Model], table_name: str, table_fields: list[Field]):
        super().__init__(instance, table_name, table_fields)
        self.__sql_values: dict = None

    @staticmethod
    def get_sql_str(values):
        """ Возвращает строку с именами полей SQL запроса """

        values_list = []
        for value in values:
            values_list.append(f'"{str(value)}"')

        return ', '.join(values_list)

    def insert_values(self, **kwargs) -> None:
        """ Выстраивает self.__values """

        self.__sql_values = kwargs

    def get_sql(self) -> str:
        assert self.__sql_values is not None, "Метод 'insert_values' не был вызван"
        sql = f'INSERT INTO {self.table_name} ({self.get_sql_str(self.__sql_values.keys())}) ' \
              f'VALUES ({self.get_sql_str(self.__sql_values.values())})'
        return sql


class GetQuery(WhereMixin, Query):
    def get_sql(self) -> str:
        # звездочку позже надо будет изменить на явное указание полей
        return f'SELECT * FROM {self.table_name}{self._where}'


class UpdateQuery(WhereMixin, Query):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__obj: Model = None

    def bind_obj(self, obj: Model):
        assert isinstance(obj, self.instance), 'Объект должен быть типом {}'.format(self.instance)
        self.__obj = obj

    def format_obj_attrs(self):
        assert self.__obj is not None, 'Необходимо вызвать метод bind_obj() прежде чем изменять данные БД'
        fields: list[str] = []

        for field in self.__obj.get_fields():
            name = field.field_name
            value = getattr(self.__obj, name, None)

            if type(value) == str:
                value = f'"{value}"'
            elif value is None:
                value = 'NULL'

            fields.append(f'{name}={value}')

        return ', '.join(fields)

    def get_sql(self):
        assert self._where is not None, 'Нужно уточнить какие таблицы будут обновлены, через метод where()'
        return f'UPDATE {self.table_name} SET {self.format_obj_attrs()}{self._where}'
