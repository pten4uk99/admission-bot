from typing import NamedTuple, Type, Iterable


class LookupParam(NamedTuple):
    field: str
    lookup_name: str = None


class Lookup:
    def __init__(self, field, value):
        self._check_right_value(field, value)
        self.field = field
        self.value = value

    def _check_right_value(self, field, value) -> None:
        """ Проверяет корректность переданного значения """

        raise NotImplementedError()

    def get_sql(self) -> str:
        """ Возвращает SQL по текущему параметру поиска """

        raise NotImplementedError()


class InLookup(Lookup):
    def _check_right_value(self, field, value):
        assert isinstance(value, Iterable), f'"value" атрибут должен быть типом {list}'

    @staticmethod
    def _wrap_item(item) -> str:
        return f'"{item}"'

    @staticmethod
    def _items_to_string(items: list) -> str:
        return ", ".join(items)

    def get_sql(self):
        items = []
        for item in self.value:
            items.append(self._wrap_item(item))

        return f'{self.field} IN ({self._items_to_string(items)})'


class LookupDispatcher:
    allowed_lookups = {
        'in': InLookup,
    }

    def __init__(self, lookup_name: str):
        self.__lookup_name = lookup_name

    def get_lookup(self) -> Type[Lookup]:
        assert self.__lookup_name in self.allowed_lookups, (
            f'Переданного параметра поиска не существует {self.__lookup_name}'
        )
        return self.allowed_lookups[self.__lookup_name]


class DunderscoreParser:
    def __init__(self, key: str, value):
        assert isinstance(key, str), f'"key" атрибут должен быть типом {str}'
        self._key = key
        self._value = value

    def _get_splitted_key(self):
        splitted = self._key.split('__')
        assert len(splitted) <= 2, f'{self._key} не может содержать более одного параметра поиска'
        return splitted

    def _lack_lookups(self, key: str) -> str:
        """ Срабатывает, если не найден дополнительный параметр поиска """

        return f'{key}={self._value}'

    def _lookup_exist(self, key: LookupParam) -> str:
        """ Срабатывает, если найден дополнительный параметр поиска  """

        lookup_class = LookupDispatcher(key.lookup_name).get_lookup()
        lookup = lookup_class(field=key.field, value=self._value)
        return lookup.get_sql()

    def get_sql(self) -> str:
        """ Возвращает часть SQL запроса, подставляющийся после ключевого слова "WHERE" """
        splitted = LookupParam(*self._get_splitted_key())

        if splitted.lookup_name is None:
            return self._lack_lookups(splitted.field)
        else:
            return self._lookup_exist(splitted)
