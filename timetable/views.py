from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
import xml.etree.ElementTree as ET

from PythonDjango.settings import BASE_DIR
from timetable.models import *
import logging

from worktime.models import Settings

logging.basicConfig(filename="log-file.log", level=logging.INFO)


# logging.info("Открыт Каталог товаров")

def viewteachers(request):
    s = Settings.objects.filter(field='timetable')[0].value
    table = Timetable.objects.get(pk=int(s))

    logging.info("!!!!!!!!       timetable/teachers.html")
    teachers = Teacher.objects.filter(timetable_id=table)
    context = {'teachers': teachers}

    return render(request, 'timetable/teachers.html', context)


def importasc(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        namefile = request.POST['namefile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        # print(uploaded_file_url)
        importgo(namefile, uploaded_file_url)
        return render(request, 'timetable/import_done.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return render(request, 'timetable/import.html')


def importgo(namefile, uploaded_file_url):
    # TODO
    # tt_id = 11  # Це прибрати перед розкоментуванням

    # Початок тимчасово закоментованого

    tree = ET.parse(BASE_DIR + uploaded_file_url)
    xml = tree.getroot()
    timetable = Timetable()
    timetable.gen_codename(uploaded_file_url)
    timetable.name = namefile
    timetable.save()
    tt_id = timetable.id

    for child in xml:
        if child.tag == "days":
            # print("Processing XML for Day")
            for d in child:
                day = Day()
                day.name = d.get("name").strip()
                day.short = d.get("short").strip()
                day.day = d.get("day").strip()
                day.timetable_id = Timetable.objects.get(pk=tt_id)
                day.save()
        elif child.tag == "periods":
            # print("Processing XML for Period")
            for d in child:
                period = Period()
                period.period = d.get("period").strip()
                period.starttime = d.get("starttime").strip()
                period.endtime = d.get("endtime").strip()
                period.timetable_id = Timetable.objects.get(pk=tt_id)
                period.save()
        elif child.tag == "teachers":
            # print("Processing XML for Teacher")
            for d in child:
                teacher = Teacher()
                teacher.ident = d.get("id").strip()
                teacher.name = d.get("name").strip()
                teacher.short = d.get("short").strip()
                teacher.gender = d.get("gender").strip()
                teacher.color = d.get("color").strip()
                teacher.timetable_id = Timetable.objects.get(pk=tt_id)
                teacher.save()
        elif child.tag == "classes":
            # print("Processing XML for Class")
            for d in child:
                clas = Class()
                clas.ident = d.get("id").strip()
                clas.name = d.get("name").strip()
                clas.short = d.get("short").strip()
                clas.classroomids = d.get("classroomids").strip()
                clas.teacherid = d.get("teacherid").strip()
                clas.timetable_id = Timetable.objects.get(pk=tt_id)
                clas.save()
        elif child.tag == "subjects":
            # print("Processing XML for Subject")
            for d in child:
                subject = Subject()
                subject.ident = d.get("id").strip()
                subject.name = d.get("name").strip()
                subject.short = d.get("short").strip()
                subject.timetable_id = Timetable.objects.get(pk=tt_id)
                subject.save()
        elif child.tag == "classrooms":
            # print("Processing XML for Classrooms")
            for d in child:
                classroom = Classroom()
                classroom.ident = d.get("id").strip()
                classroom.name = d.get("name").strip()
                classroom.short = d.get("short").strip()
                classroom.timetable_id = Timetable.objects.get(pk=tt_id)
                classroom.save()

        elif child.tag == "groups":
            # print("Processing XML for Group")
            for d in child:  # classid,name,entireclass,divisiontag,studentcount
                group = Group()
                group.ident = d.get("id").strip()
                group.name = d.get("name").strip()
                group.classid = d.get("classid").strip()
                group.entireclass = d.get("entireclass").strip()
                group.divisiontag = d.get("divisiontag").strip()
                group.studentcount = d.get("studentcount").strip()
                group.timetable_id = Timetable.objects.get(pk=tt_id)
                group.save()
        elif child.tag == "lessons":
            # print("Processing XML for Lesson")
            for d in child:  # id,subjectid,classids,groupids,studentids,teacherids,classroomids,periodspercard,periodsperweek,weeks
                lesson = Lesson()
                lesson.ident = d.get("id").strip()
                lesson.subjectid = d.get("subjectid").strip()
                lesson.classids = d.get("classids").strip()
                lesson.groupids = d.get("groupids").strip()
                lesson.studentids = d.get("studentids").strip()
                lesson.teacherids = d.get("teacherids").strip()
                lesson.classroomids = d.get("classroomids").strip()
                lesson.periodspercard = d.get("periodspercard").strip()
                lesson.periodsperweek = d.get("periodsperweek").strip()
                lesson.weeks = d.get("weeks").strip()
                lesson.timetable_id = Timetable.objects.get(pk=tt_id)
                lesson.save()
        elif child.tag == "cards":
            # print("Processing XML for Card")
            for d in child:  # lessonid,day,period,classroomids
                card = Card()
                ss = d.get("lessonid").strip()
                l = Lesson.objects.filter(timetable_id=tt_id, ident=ss)
                per = l[0].id
                card.lesson_id = l.get(pk=per)
                ss = d.get("day").strip()
                l = Day.objects.filter(timetable_id=tt_id, day=ss)
                per = l[0].id
                card.day_id = l.get(pk=per)
                ss = d.get("period").strip()
                l = Period.objects.filter(timetable_id=tt_id, period=ss)
                per = l[0].id
                card.period_id = l.get(pk=per)
                card.classroomids = d.get("classroomids").strip()
                card.timetable_id = Timetable.objects.get(pk=tt_id)
                card.save()

    # Кінець тимчасово закоментованого

    # Заповнюємо ManyToMany поля
    # Для поля Class
    # print("Processing ManyToMany for Class")
    classes = Class.objects.filter(timetable_id=tt_id)
    for clas in classes:
        rooms = clas.classroomids.split(',')
        for room in rooms:
            if room != '':
                per = Classroom.objects.filter(timetable_id=tt_id, ident=room)[0]
                i_id = per.id
                clas.classrooms.add(Classroom.objects.get(pk=i_id))
        clas.save()

    # teachers = models.ManyToManyField('Teacher')

    # Для поля Lesson
    # print("Processing ManyToMany for Lesson")
    lessons = Lesson.objects.filter(timetable_id=tt_id)
    for lesson in lessons:
        # print(lesson.classids)
        ls = lesson.subjectid.split(',')
        for l in ls:
            if l != '':
                per = Subject.objects.filter(timetable_id=tt_id, ident=l)[0]
                i_id = per.id
                lesson.subjects.add(Subject.objects.get(pk=i_id))
        ls = lesson.classids.split(',')
        for l in ls:
            if l != '':
                per = Class.objects.filter(timetable_id=tt_id, ident=l)[0]
                i_id = per.id
                lesson.classes.add(Class.objects.get(pk=i_id))
        ls = lesson.groupids.split(',')
        for l in ls:
            if l != '':
                per = Group.objects.filter(timetable_id=tt_id, ident=l)[0]
                i_id = per.id
                lesson.groups.add(Group.objects.get(pk=i_id))
        ls = lesson.teacherids.split(',')
        for l in ls:
            if l != '':
                per = Teacher.objects.filter(timetable_id=tt_id, ident=l)[0]
                i_id = per.id
                lesson.teachers.add(Teacher.objects.get(pk=i_id))
        ls = lesson.classroomids.split(',')
        for l in ls:
            if l != '':
                per = Classroom.objects.filter(timetable_id=tt_id, ident=l)[0]
                i_id = per.id
                lesson.classrooms.add(Classroom.objects.get(pk=i_id))
        lesson.save()

    # Для поля Group
    # print("Processing ManyToMany for Group")
    groups = Group.objects.filter(timetable_id=tt_id)
    for group in groups:
        cls = group.classid.split(',')
        for cl in cls:
            if cl != '':
                per = Class.objects.filter(timetable_id=tt_id, ident=cl)[0]
                i_id = per.id
                group.classes.add(Class.objects.get(pk=i_id))
        group.save()

    #
    # # Для поля Card
    # print("Processing ManyToMany for Card")
    cards = Card.objects.filter(timetable_id=tt_id)
    for card in cards:
        # print(lesson.classids)
        ls = card.classroomids.split(',')
        for l in ls:
            if l != '':
                per = Classroom.objects.filter(timetable_id=tt_id, ident=l)[0]
                i_id = per.id
                card.classrooms.add(Classroom.objects.get(pk=i_id))
        card.save()


# Скрипти для очистки

"""

delete from timetable_card where true;
delete from timetable_card_classrooms where true;
delete from timetable_class where true;
delete from timetable_class_classrooms where true;
delete from timetable_class_teachers where true;
delete from timetable_classroom where true;
delete from timetable_day where true;
delete from timetable_group where true;
delete from timetable_group_classes where true;
delete from timetable_lesson where true;
delete from timetable_lesson_classes where true;
delete from timetable_lesson_classrooms where true;
delete from timetable_lesson_groups where true;
delete from timetable_lesson_subjects where true;
delete from timetable_lesson_teachers where true;
delete from timetable_period where true;
delete from timetable_subject where true;
delete from timetable_teacher where true;
delete from timetable_timetable where true;

"""
