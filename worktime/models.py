from django.db import models

class Worktimetable(models.Model):  # Таблиця містить вказівники на плани, які є в базі
    name = models.CharField(null=True, blank=True, max_length=150)
    acyear_id = models.ForeignKey('Academyear', default=None, blank=True, null=True, on_delete=models.PROTECT)

class Workday(models.Model):
    num = models.IntegerField(null=False)
    wday = models.DateField(null=False, verbose_name="Дата")
    numworkweek = models.IntegerField(null=False)
    dayweek = models.IntegerField(null=False)
    weekchzn = models.IntegerField(null=False, verbose_name="1-чис., 2-зн., 0-вихідний")
    worktimeable = models.ForeignKey('Worktimetable', default=None, blank=True, null=True, on_delete=models.PROTECT)

class Academyear(models.Model):
    name = models.CharField(null=False, blank=False, max_length=15)



class Vacat(models.Model):
    date = models.DateField(null=False, blank=False, verbose_name="Date of vacation")
    name = models.CharField(default='', null=True, blank=True, max_length=15)
    deleted = models.BooleanField(default=False, null=False)
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
