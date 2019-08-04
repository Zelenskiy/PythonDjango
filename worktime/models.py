from django.db import models


# from timetable.models import *

class Worktimetable(models.Model):  # Таблиця містить вказівники на плани, які є в базі
    name = models.CharField(null=True, blank=True, max_length=150)
    acyear_id = models.ForeignKey('Academyear', default=None, blank=True, null=True, on_delete=models.PROTECT)


class Replacement(models.Model):
    missteach = models.ForeignKey('timetable.Teacher', related_name='miss_teacher', default=None, blank=False,
                                  null=False, on_delete=models.PROTECT)
    replteach = models.ForeignKey('timetable.Teacher', related_name='repl_teacher', default=None, blank=True, null=True,
                                  on_delete=models.PROTECT)
    date = models.DateTimeField(db_index=True, verbose_name='Дата пропуску')
    clas = models.ForeignKey('timetable.Class', default=None, blank=False, null=False, on_delete=models.PROTECT)
    misssubj = models.ForeignKey('timetable.Subject', related_name='miss_subj', default=None, blank=False, null=False,
                                 on_delete=models.PROTECT)
    replsubj = models.ForeignKey('timetable.Subject', related_name='repl_subj', default=None, blank=True, null=True,
                                 on_delete=models.PROTECT)
    reason = models.CharField(null=True, blank=True, max_length=15)
    published = models.DateTimeField(auto_now=True, db_index=True, verbose_name='Опубліковано')
    worktimeable = models.ForeignKey('Worktimetable', default=None, blank=True, null=True, on_delete=models.PROTECT)


class Missing(models.Model):
    teach = models.ForeignKey('timetable.Teacher', default=None, blank=False, null=False, on_delete=models.PROTECT,
                              verbose_name='Відсутній вчитель')
    date_st = models.DateTimeField(db_index=True, verbose_name='Відсутній з')
    date_fin = models.DateTimeField(db_index=True, verbose_name='Відсутній по')
    reason = models.CharField(null=True, blank=True, max_length=15, verbose_name='Причина відсутності')
    kl_ker = models.BooleanField(default=True, null=False, blank=True, verbose_name='Класний керівник')
    poch_kl = models.BooleanField(default=False, null=False, blank=True, verbose_name='Викладає в початкових класах')
    published = models.DateTimeField(auto_now=True, db_index=True, verbose_name='Опубліковано')
    worktimeable = models.ForeignKey('Worktimetable', default=None, blank=True, null=True, on_delete=models.PROTECT)

    class Meta:
        ordering = ['-published']


class Workday(models.Model):
    num = models.IntegerField(null=False)
    wday = models.DateField(null=False, verbose_name="Дата")
    numworkweek = models.IntegerField(null=False)
    dayweek = models.IntegerField(null=False)
    weekchzn = models.IntegerField(null=False, verbose_name="1-чис., 2-зн., 0-вихідний")
    # TODO Тут допилять додавання цього поля при генерації
    worktimetable = models.ForeignKey('Worktimetable', default=None, blank=True, null=True, on_delete=models.PROTECT)
    acyear_id = models.ForeignKey('Academyear', default=None, blank=True, null=True, on_delete=models.PROTECT)


class Academyear(models.Model):
    name = models.CharField(null=False, blank=False, max_length=15)


class Vacat(models.Model):
    date = models.DateField(null=False, blank=False, verbose_name="Date of vacation")
    name = models.CharField(default='', null=True, blank=True, max_length=15)
    deleted = models.BooleanField(default=False, null=False)
    # TODO Тут допилять додавання цього поля при генерації
    worktimetable = models.ForeignKey('Worktimetable', default=None, blank=True, null=True, on_delete=models.PROTECT)

    acyear_id = models.ForeignKey('Academyear', default=0, blank=False, null=False, on_delete=models.PROTECT)
    published = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        ordering = ['date', 'published']


class Settings(models.Model):
    field = models.CharField(null=False, blank=False, max_length=15)
    verbose = models.CharField(default='', null=True, blank=True, max_length=15)
    value = models.CharField(null=False, blank=False, max_length=250)
    published = models.DateTimeField(auto_now=True, db_index=True, verbose_name='Опубліковано')
    sort = models.FloatField(default=0)

    class Meta:
        ordering = ['sort', 'published']
