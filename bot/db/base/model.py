__all__ = [
    'Model'
]


class Model:
    query_ = None
    fields_ = []
    __pk = None

    def __init__(self, **kwargs):
        assert self.fields_, 'Список полей модели {} не сформирован'.format(self.__class__)

        for field in self.fields_:
            value = kwargs.get(field.field_name, None)
            if value is not None and value != 'None':
                setattr(self, field.field_name, value)

        assert self.pk_field is not None, 'Не установлен атрибут pk_field для {}'.format(self.__class__)
        self.pk_ = kwargs.get(self.pk_field)

    @property
    def pk_field(self):
        return self.__pk

    @pk_field.setter
    def pk_field(self, value):
        assert hasattr(self, value), "Невозможно указать несуществующее поле модели в качестве primary_key"
        self.__pk = value

    def save(self):
        self.query_.instance = self
        pk_dict = {self.pk_field: self.pk_}
        self.query_.update(**pk_dict)
        self.query_.perform_update()
