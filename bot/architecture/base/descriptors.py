class MessageCallbackDescriptor:
    def __set_name__(self, owner, name):
        self.name = name
    
    def __get__(self, instance, owner):
        return instance.__dict__.get(self.name, None)
    
    def __set__(self, instance, value):
        if value is not None:
            assert callable(value), (
                'Атрибут "{}" '
                'класса {} должен быть Callable'.format(self.name, self.__class__.__name__)
            )
        instance.__dict__[self.name] = value


class ButtonMessageCallbackDescriptor(MessageCallbackDescriptor):
    def __get__(self, instance, owner):
        if instance.__dict__[self.name] is None:
            async def none_callback(message):
                pass
            
            return none_callback
        return instance.__dict__[self.name]
    
    def __set__(self, instance, value):
        if value is not None:
            assert callable(value), (
                'Атрибут "{}" '
                'класса {} должен быть Callable'.format(self.name, instance.__class__.__name__)
            )
        
        if 'override_callback' not in instance.__dict__:
            instance.__dict__[self.name] = value