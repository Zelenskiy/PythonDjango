from django.db import models
from worktime.models import Academyear


class Plantable(models.Model):  # Таблиця містить вказівники на плани, які є в базі
    name = models.CharField(null=True, blank=True, max_length=150)
    acyear_id = models.ForeignKey('worktime.Academyear', default=None, blank=True, null=True, on_delete=models.PROTECT)



class Plan(models.Model):
    # r_id = models.IntegerField(null=True, blank=True, verbose_name='')
    r_id = models.ForeignKey('Rubric', default=None, null=True, blank=True, verbose_name='Розділ',
                             on_delete=models.PROTECT)
    content = models.TextField(null=True, blank=True, verbose_name='Опис')
    termin = models.CharField(null=True, blank=True, max_length=150, verbose_name='Строки виконання')
    generalization = models.CharField(null=True, blank=True, max_length=50, verbose_name='Форма узагальнення')
    responsible = models.CharField(null=True, blank=True, max_length=150, verbose_name='Відповідальний')
    note = models.CharField(null=True, blank=True, max_length=50, verbose_name='Примітка')
    sort = models.FloatField(null=True, blank=True, verbose_name='Порядок сортування')
    # direction_id = models.IntegerField(null=True, blank=True, verbose_name='Напрямок')
    # purpose_id = models.IntegerField(null=True, blank=True, verbose_name='Мета')
    direction_id = models.ForeignKey('Direction', default=None, blank=True, null=True, on_delete=models.PROTECT,
                                     verbose_name='Напрямок')
    purpose_id = models.ForeignKey('Purpose', default=None, null=True, blank=True, on_delete=models.PROTECT,
                                   verbose_name='Мета')
    show = models.BooleanField(default=True, null=False, blank=True, verbose_name='Відображати у звіті')
    published = models.DateTimeField(auto_now=True, db_index=True, verbose_name='Опубліковано')
    done = models.BooleanField(default=False, null=False, blank=True, verbose_name='Відмітка про виконання')
    #tmp = models.CharField(max_length=50, null=True, blank=True, verbose_name='tmp')
    #tmp2 = models.CharField(max_length=50, null=True, blank=True, verbose_name='tmp')
    plantable_id = models.ForeignKey('Plantable', default=None, null=True, blank=True, on_delete=models.PROTECT)
    #published = models.DateTimeField(auto_now=True, db_index=True, verbose_name='Опубликовано')

    #rubric    = models.CharField(null=True, blank=True, max_length=10)
    #direction = models.CharField(null=True, blank=True, max_length=10)
    #purpose   = models.CharField(null=True, blank=True, max_length=10)

    class Meta:
        ordering = ['direction_id', 'sort']


class Direction(models.Model):
    name = models.CharField(max_length=50, verbose_name='Напрямок', null=True, blank=True, )
    #ident = models.CharField(max_length=10, null=True, blank=True)
    published = models.DateTimeField(auto_now=True, db_index=True, verbose_name='Опубликовано')
    plantable_id = models.ForeignKey('Plantable', default=None, null=False, blank=True, on_delete=models.PROTECT)

    def __str__(self):
        return self.name


class Responsibl(models.Model):
    name = models.CharField(max_length=150, verbose_name='Мета', null=True, blank=True)
    plan_id = models.ForeignKey('Plan', null=True, on_delete=models.PROTECT, verbose_name='')
    #ident = models.CharField(max_length=10, null=True, blank=True)
    published = models.DateTimeField(auto_now=True, db_index=True, verbose_name='Опубликовано')
    plantable_id = models.ForeignKey('Plantable', default=None, null=False, blank=True, on_delete=models.PROTECT)

    def __str__(self):
        return self.name


class Terms(models.Model):
    name = models.CharField(max_length=50, verbose_name='Назва події')
    start = models.DateField(null=True, blank=True, verbose_name='Початок події')
    finish = models.DateField(null=True, blank=True, verbose_name='Кінець події')
    plan_id = models.ForeignKey('Plan', null=True, on_delete=models.PROTECT, verbose_name='')
    tmp = models.IntegerField(null=True, blank=True, verbose_name='')
    published = models.DateTimeField(auto_now=True, db_index=True, verbose_name='Опубликовано')
    plantable_id = models.ForeignKey('Plantable', default=None, null=False, blank=True, on_delete=models.PROTECT)

    # Якщо  start не None а finish = None                           До 01.09.19
    # Якщо  start None а finish не None                             01.09.19
    # Якщо  start не None і finish не None                          З 01.09.19 по 05.09.19
    # Якщо  start є першим днем року, а finish - останнім           Протягом року
    # Якщо  start пешрий день місяця, а finish останній             Вересень 2019

    def __str__(self):
        return self.name


class Purpose(models.Model):
    name = models.CharField(max_length=50, verbose_name='Мета')
    #ident = models.IntegerField(null=True, blank=True, verbose_name='')
    published = models.DateTimeField(auto_now=True, db_index=True, verbose_name='Опубликовано')
    plantable_id = models.ForeignKey('Plantable', default=None, null=False, blank=True, on_delete=models.PROTECT)

    # tmp = models.IntegerField(null=True, blank=True, verbose_name='')

    def __str__(self):
        return self.name


class Rubric(models.Model):
    name = models.CharField(null=True, blank=True, max_length=50, verbose_name='Розділ')
    n_r = models.IntegerField(null=True, blank=True, verbose_name='')
    id_owner = models.ForeignKey('self', null=True, on_delete=models.PROTECT, verbose_name='')
    riven = models.IntegerField(null=True, blank=True, verbose_name='')
    #ident = models.CharField(null=True, blank=True, max_length=10)
    #ownertmp = models.CharField(null=True, blank=True, max_length=10)
    published = models.DateTimeField(auto_now=True, db_index=True, verbose_name='Опубликовано')
    plantable_id = models.ForeignKey('Plantable', default=None, null=False, blank=True, on_delete=models.PROTECT)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['n_r']
