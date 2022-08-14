class ButtonException(Exception):
    pass


class SingleHandlerMethodException(ButtonException):
    """ В классе может быть только один обработчик """