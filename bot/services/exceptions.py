class AnalyzerException(Exception):
    pass


class WrongReferent(AnalyzerException):
    """ Неверный объект результата анализа """
