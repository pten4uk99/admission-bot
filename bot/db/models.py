from db import base as models


class Student(models.Model):
    chat_id = models.IntegerField(pk=True, null=False)
    language = models.CharField()
    russian_nationality = models.CharField()
    study_decree = models.CharField()
    study_form = models.CharField()
    profession = models.CharField()

