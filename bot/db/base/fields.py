import importlib

import config
from db.base.backends import Backend
from db.base.utils import camel_to_snake

backends = importlib.import_module(config.DEFAULT_BACKEND_DIR)
backend = getattr(backends, config.DATABASE['ENGINE'])


class Field:
    """
    Класс поля, который используется в описании моделей БД.

    При наследовании:
    self.SQL_TYPE - обязательный атрибут. Представляет название одного из атрибутов DBFieldTypes.

    Использование:
    self.to_sql() - Возвращает SQL строку, описывающую данное поле для создания таблицы БД
    """

    SQL_TYPE: str = None
    foreign_key = False
    db_backend: Backend = backend()

    def __init__(self, pk: bool = False, null: bool = True):
        self.sql_kwargs = self.get_sql_kwargs(pk, null)
        self.is_pk = pk

    def __set_name__(self, owner, name):
        self.field_name = name

        if self.is_pk:
            owner.pk_field = self.field_name

    def __get__(self, instance, owner):
        return instance.__dict__.get(self.field_name, None)

    def __set__(self, instance, value):
        instance.__dict__[self.field_name] = value

    def __repr__(self):
        return f'<Поле: "{self.field_name}" типа {self.__class__}>'

    def get_foreign_key_sql(self):
        raise NotImplemented()

    def get_sql_kwargs(self, pk: bool, null: bool) -> str:
        """ Возвращает строку с дополнительными параметрами SQL описания поля. """

        result = ''
        if pk:
            result += ' PRIMARY KEY AUTOINCREMENT'
        if not null:
            result += ' NOT NULL'
        return result

    def get_sql_type(self):
        assert self.SQL_TYPE is not None, 'Обязательный атрибут класса SQL_TYPE'
        return self.SQL_TYPE

    def to_sql(self) -> str:
        """ Возвращает строку SQL запроса для текущего поля """

        assert self.db_backend is not None, 'Не назначен атрибут "db_backend"'

        field_type = getattr(self.db_backend.types, self.get_sql_type(), None)
        assert field_type is not None, 'Тип поля не может быть None'

        return f'{self.field_name} {field_type}{self.sql_kwargs}'


class CharField(Field):
    SQL_TYPE = 'STRING'


class IntegerField(Field):
    SQL_TYPE = 'NUMBER'


class ForeignKeyField(Field):
    """
    self.foreign_key - является ли поле связанным с другой таблицей.
    """

    SQL_TYPE = 'NUMBER'
    foreign_key = True

    def __init__(self, to: str, pk: bool = False, null: bool = True):
        super().__init__(pk=pk, null=null)
        self.to = camel_to_snake(to)

    def get_foreign_key_sql(self):
        return f'FOREIGN KEY ({self.field_name}) REFERENCES {self.to}(pk) ON DELETE CASCADE'

