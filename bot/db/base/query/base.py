from typing import Type

from db.base import Model
from db.base import Field


class Query:
    def __init__(self, instance: Type[Model], table_name: str, table_fields: list[Field]):
        self.instance = instance
        self.table_name = table_name
        self.table_fields = table_fields

    def get_sql(self) -> str:
        """ Формирует SQL запрос """

        raise NotImplementedError()
