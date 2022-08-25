class WhereMixin:
    """
    Добавляет к основному классу фильтрацию.

    При наследовании:
    self._where - атрибут, который хранит строку с SQL запросом по фильтрации

    Использование:
    self.where() - метод, который формирует SQL строку
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._where = ''

    def where(self, **kwargs) -> None:
        """ В kwargs ожидаются поля модели и их значения """

        if kwargs:
            where = ' WHERE'
            values = []

            for key, value in kwargs.items():
                string = f'{key}={value}'
                values.append(string)

            string_values = ' AND'.join(values)
            self._where = f'{where} {string_values}'
