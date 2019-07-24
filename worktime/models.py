from django.db import models

class Worktimetable(models.Model):  # Таблиця містить вказівники на плани, які є в базі
    name = models.CharField(null=True, blank=True, max_length=150)

class Workday(models.Model):
    num             = models.IntegerField(null=False)
    wday            = models.DateField(null=False, verbose_name="Дата")
    numworkweek     = models.IntegerField(null=False)
    dayweek         = models.IntegerField(null=False)
    weekchzn        = models.IntegerField(null=False, verbose_name="1-чис., 2-зн., 0-вихідний")
    worktimeable    = models.ForeignKey('Worktimetable', default=None, blank=True, null=True, on_delete=models.PROTECT)

class Settings(models.Model):
    field = models.CharField(null=False, blank=False, max_length=15)
    value = models.CharField(null=False, blank=False, max_length=250)
    published = models.DateTimeField(auto_now=True, db_index=True, verbose_name='Опубліковано')
