from django.db import models

class Day(models.Model):
    day = models.CharField(max_length=10)
    name = models.CharField(max_length=20)
    short = models.CharField(max_length=10)

    class Meta:
        ordering = ['day']

class Period(models.Model):
    period = models.CharField(max_length=10)
    starttime = models.CharField(max_length=10)
    endtime = models.CharField(max_length=10)

    class Meta:
        ordering = ['period']


class Teacher(models.Model):
    ident = models.CharField(max_length=10)
    name = models.CharField(max_length=30)
    short = models.CharField(max_length=10)
    gender = models.CharField(max_length=10)
    color = models.CharField(max_length=10)
    sort = models.FloatField(default=0, null=True, blank=True, verbose_name='Порядок сортування')

    class Meta:
        ordering = ['sort']


class Class(models.Model):
    classroom_id = models.ForeignKey('Classroom', default=None, blank=True, null=True, on_delete=models.PROTECT)
    teacher_id = models.ForeignKey('Teacher', default=None, blank=True, null=True, on_delete=models.PROTECT)
    ident = models.CharField(max_length=10)
    name = models.CharField(max_length=10)
    short = models.CharField(max_length=5)
    sort = models.FloatField(default=0, null=True, blank=True, verbose_name='Порядок сортування')

    class Meta:
        ordering = ['sort']

    # classroomids = models.CharField(max_length=10)
    # teacherid = models.CharField(max_length=10)


class Subject(models.Model):
    ident = models.CharField(max_length=10)
    name = models.CharField(max_length=30)
    short = models.CharField(max_length=10)
    sort = models.FloatField(default=0, null=True, blank=True, verbose_name='Порядок сортування')

    class Meta:
        ordering = ['sort']

class Classroom(models.Model):
    ident = models.CharField(max_length=10)
    name = models.CharField(max_length=10)
    short = models.CharField(max_length=5)
    sort = models.FloatField(default=0, null=True, blank=True, verbose_name='Порядок сортування')

    class Meta:
        ordering = ['sort']



class Group(models.Model):
    class_id = models.ForeignKey('Class', default=None, blank=True, null=True, on_delete=models.PROTECT)
    name = models.CharField(max_length=10)
    entireclass = models.CharField(max_length=10)
    divisiontag = models.CharField(max_length=10)
    studentcount = models.CharField(max_length=10)
    ident = models.CharField(max_length=10)
    sort = models.FloatField(default=0, null=True, blank=True, verbose_name='Порядок сортування')

    class Meta:
        ordering = ['sort']

    # classid = models.CharField(max_length=10)

class Lesson(models.Model):
    subject_id = models.ForeignKey('Subject', default=None, blank=True, null=True, on_delete=models.PROTECT)
    class_id = models.ForeignKey('Class', default=None, blank=True, null=True, on_delete=models.PROTECT)
    group_id = models.ForeignKey('Group', default=None, blank=True, null=True, on_delete=models.PROTECT)
    teacher_id = models.ForeignKey('Teacher', default=None, blank=True, null=True, on_delete=models.PROTECT)
    classroom_id = models.ForeignKey('Classroom', default=None, blank=True, null=True, on_delete=models.PROTECT)
    periodspercard = models.CharField(max_length=10)
    periodsperweek = models.CharField(max_length=10)
    weeks = models.CharField(max_length=10)
    ident = models.CharField(max_length=10)
    sort = models.FloatField(default=0, null=True, blank=True, verbose_name='Порядок сортування')

    class Meta:
        ordering = ['sort']

    # subjectid = models.CharField(max_length=10)
    # classids = models.CharField(max_length=10)
    # groupids = models.CharField(max_length=10)
    # studentids = models.CharField(max_length=10)
    # teacherids = models.CharField(max_length=10)
    # classroomids = models.CharField(max_length=10)


class Card(models.Model):
    classroom_id = models.ForeignKey('Classroom', default=None, blank=True, null=True, on_delete=models.PROTECT)
    lesson_id = models.ForeignKey('Lesson', default=None, blank=True, null=True, on_delete=models.PROTECT)
    day_id = models.ForeignKey('Day', default=None, blank=True, null=True, on_delete=models.PROTECT)
    period_id = models.ForeignKey('Period', default=None, blank=True, null=True, on_delete=models.PROTECT)


    # lessonid = models.CharField(max_length=10)
    # day = models.CharField(max_length=5)
    # period = models.CharField(max_length=5)
    # classroomids = models.CharField(max_length=10)







