from db import base as models


class Student(models.Model):
    chat_id = models.IntegerField(pk=True, null=False)
    language = models.CharField()
    russian_nationality = models.CharField()
    study_degree = models.CharField()
    study_form = models.CharField()
    profession = models.CharField()


class Keyword(models.Model):
    """ Ключевое слово """

    pk = models.IntegerField(pk=True, null=False)
    comparison = models.ForeignKeyField('Comparison')
    source = models.CharField()
    normalized = models.CharField()


class Comparison(models.Model):
    """ Сопоставление ключевых слов и ответа """

    pk = models.IntegerField(pk=True, null=False)
    answer = models.CharField()

