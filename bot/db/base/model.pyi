from db.base import Field
from db.base.query.query_factory import SQLFactory


class Model:
    query_: SQLFactory
    fields_: list[Field]
    ...