from time import time

from django.db import models
from django.utils.text import slugify


class Timetable(models.Model):
    codename = models.SlugField(null=False, max_length=150, unique=True, default="", verbose_name='Slug')
    name = models.CharField(blank=True, null=True, max_length=20)
    acyear_id = models.ForeignKey('worktime.Academyear', default=None, blank=True, null=True, on_delete=models.PROTECT)

    def gen_codename(self, s):
        self.codename = slugify(s, allow_unicode=True)+'-'+str(int(time()))

class Day(models.Model):
    day = models.CharField(max_length=10)
    name = models.CharField(max_length=20)
    short = models.CharField(max_length=10)
    timetable_id = models.ForeignKey('Timetable', default=None, blank=True, null=True, on_delete=models.PROTECT)

    class Meta:
        ordering = ['day']

class Period(models.Model):
    period = models.CharField(max_length=10)
    starttime = models.CharField(max_length=10)
    endtime = models.CharField(max_length=10)
    timetable_id = models.ForeignKey('Timetable', default=None, blank=True, null=True, on_delete=models.PROTECT)

    class Meta:
        ordering = ['period']


class Teacher(models.Model):
    ident = models.CharField(max_length=10)
    name = models.CharField(max_length=30)
    short = models.CharField(max_length=10)
    gender = models.CharField(max_length=10)
    color = models.CharField(max_length=10)
    sort = models.FloatField(default=0, null=True, blank=True, verbose_name='Порядок сортування')
    timetable_id = models.ForeignKey('Timetable', default=None, blank=True, null=True, on_delete=models.PROTECT)
    def __str__(self):
        return self.short
    class Meta:
        ordering = ['sort']


class Class(models.Model):
    classrooms = models.ManyToManyField('Classroom')
    teachers = models.ManyToManyField('Teacher')
    ident = models.CharField(max_length=10)
    name = models.CharField(max_length=10)
    short = models.CharField(max_length=5)
    sort = models.FloatField(default=0, null=True, blank=True, verbose_name='Порядок сортування')
    timetable_id = models.ForeignKey('Timetable', default=None, blank=True, null=True, on_delete=models.PROTECT)

    classroomids = models.CharField(max_length=10, null=True, blank=True)
    teacherid = models.CharField(max_length=10, null=True, blank=True)

    class Meta:
        ordering = ['sort']




class Subject(models.Model):
    ident = models.CharField(max_length=10)
    name = models.CharField(max_length=30)
    short = models.CharField(max_length=10)
    sort = models.FloatField(default=0, null=True, blank=True, verbose_name='Порядок сортування')
    timetable_id = models.ForeignKey('Timetable', default=None, blank=True, null=True, on_delete=models.PROTECT)

    class Meta:
        ordering = ['sort']

class Classroom(models.Model):
    ident = models.CharField(max_length=10)
    name = models.CharField(max_length=10)
    short = models.CharField(max_length=5)
    sort = models.FloatField(default=0, null=True, blank=True, verbose_name='Порядок сортування')
    timetable_id = models.ForeignKey('Timetable', default=None, blank=True, null=True, on_delete=models.PROTECT)

    class Meta:
        ordering = ['sort']



class Group(models.Model):
    classes = models.ManyToManyField('Class')
    name = models.CharField(max_length=10)
    entireclass = models.CharField(max_length=10)
    divisiontag = models.CharField(max_length=10)
    studentcount = models.CharField(max_length=10)
    ident = models.CharField(max_length=10)
    sort = models.FloatField(default=0, null=True, blank=True, verbose_name='Порядок сортування')
    timetable_id = models.ForeignKey('Timetable', default=None, blank=True, null=True, on_delete=models.PROTECT)

    classid = models.CharField(max_length=10, null=True, blank=True)

    class Meta:
        ordering = ['sort']



class Lesson(models.Model):
    # subject_id = models.ForeignKey('Subject', default=None, blank=True, null=True, on_delete=models.PROTECT)
    subjects = models.ManyToManyField('Subject')
    classes = models.ManyToManyField('Class')
    groups = models.ManyToManyField('Group')
    teachers = models.ManyToManyField('Teacher')
    classrooms = models.ManyToManyField('Classroom')
    periodspercard = models.CharField(max_length=10)
    periodsperweek = models.CharField(max_length=10)
    weeks = models.CharField(max_length=10)
    ident = models.CharField(max_length=10)
    sort = models.FloatField(default=0, null=True, blank=True, verbose_name='Порядок сортування')
    timetable_id = models.ForeignKey('Timetable', default=None, blank=True, null=True, on_delete=models.PROTECT)

    subjectid = models.CharField(max_length=10, null=True, blank=True)
    classids = models.CharField(max_length=10, null=True, blank=True)
    groupids = models.CharField(max_length=10, null=True, blank=True)
    studentids = models.CharField(max_length=10, null=True, blank=True)
    teacherids = models.CharField(max_length=10, null=True, blank=True)
    classroomids = models.CharField(max_length=10, null=True, blank=True)

    class Meta:
        ordering = ['sort']




class Card(models.Model):
    classrooms = models.ManyToManyField('Classroom')
    lesson_id = models.ForeignKey('Lesson', default=None, blank=True, null=True, on_delete=models.PROTECT)
    day_id = models.ForeignKey('Day', default=None, blank=True, null=True, on_delete=models.PROTECT)
    period_id = models.ForeignKey('Period', default=None, blank=True, null=True, on_delete=models.PROTECT)
    timetable_id = models.ForeignKey('Timetable', default=None, blank=True, null=True, on_delete=models.PROTECT)


    # lessonid = models.CharField(max_length=10, null=True, blank=True)
    classroomids = models.CharField(max_length=10, null=True, blank=True)







