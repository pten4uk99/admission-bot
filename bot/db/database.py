import importlib
from typing import Type

import config
from db.base import Model
from db.base.backends import Backend
from db.base.query.query_factory import SQLFactory

backends = importlib.import_module(config.DEFAULT_BACKEND_DIR)
backend = getattr(backends, config.DATABASE['ENGINE'])


class DataBase:
    db_backend: Type[Backend] = backend

    def __init__(self):
        self.backend = self.db_backend()
        self.connection = None

    def check_connection(self):
        assert self.connection is not None, 'Подключение к БД не еще не было установлено'

    def create_tables(self):
        self.check_connection()

        import inspect
        import db.models as models

        for name, model in inspect.getmembers(models):
            model: Type[Model]
            if inspect.isclass(model):
                model.query_ = SQLFactory(instance_class=model, db_backend=self.backend, connection=self.connection)
                model.query_.create_table()
                model.query_.perform_update()

        self.connection.commit()

    def connect(self):
        if self.connection is None:
            self.connection = self.backend.connect()

    def close(self):
        if self.connection is not None:
            self.connection.close()


if __name__ == '__main__':
    pass
