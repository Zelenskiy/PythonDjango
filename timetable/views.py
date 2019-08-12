import codecs

from django.core.files.storage import FileSystemStorage
from django.db.models import Q
from django.shortcuts import render
import xml.etree.ElementTree as ET

from PythonDjango.settings import BASE_DIR
from timetable.models import *
import logging

from worktime.models import Settings, Missing, Hourlyworker

# logging.basicConfig(filename="log-file.log", level=logging.INFO)


# logging.info("Открыт Каталог товаров")

def viewteachers(request):
    s = Settings.objects.filter(field='timetable')[0].value
    table = Timetable.objects.get(pk=int(s))

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
    # Чистимо старі бази
    Missing.objects.all().delete()
    Hourlyworker.objects.all().delete()
    Card.objects.all().delete()
    Class.objects.all().delete()
    Classroom.objects.all().delete()
    Teacher.objects.all().delete()
    Day.objects.all().delete()
    Group.objects.all().delete()
    Lesson.objects.all().delete()
    Period.objects.all().delete()
    Resp.objects.all().delete()
    Subject.objects.all().delete()
    Timetable.objects.all().delete()


    # Початок тимчасово закоментованого

    # tree = ET.parse(BASE_DIR + uploaded_file_url)
    # tree = ET.parse('d:/MyDoc/PythonDjango/asc_cp1251.xml')
    # filename = 'd:/MyDoc/PythonDjango/asc_cp1251.xml'
    # namefile = 'aaa'
    # uploaded_file_url = 'aaa'


    filename = BASE_DIR + uploaded_file_url
    tree = ET.parse(codecs.open(filename, 'rb', 'cp1251'))
    # tree = ET.parse((filename))

    xml = tree.getroot()
    timetable = Timetable()
    timetable.gen_codename(uploaded_file_url)
    timetable.name = namefile
    timetable.save()
    tt_id = timetable.id

    teacher_ident = {}
    class_ident = {}
    class_classroomids = {}
    class_teacherid = {}
    subject_ident = {}
    classroom_ident = {}
    group_ident = {}
    group_classid = {}
    lesson_ident = {}

    lesson_subjectid    = {}
    lesson_classids    = {}
    lesson_groupids    = {}
    lesson_studentids    = {}
    lesson_teacherids    = {}
    lesson_classroomids    = {}

    for child in xml:
        if child.tag == "days":
            print(" Processing XML for Day")
            for d in child:
                day = Day()
                day.name = d.get("name").strip()
                day.short = d.get("short").strip()
                day.day = d.get("day").strip()
                day.timetable_id = Timetable.objects.get(pk=tt_id)
                day.save()
        elif child.tag == "periods":
            print(" Processing XML for Period")
            for d in child:
                period = Period()
                period.period = d.get("period").strip()
                period.starttime = d.get("starttime").strip()
                period.endtime = d.get("endtime").strip()
                period.timetable_id = Timetable.objects.get(pk=tt_id)
                period.save()
        elif child.tag == "teachers":
            i = 0
            print('\n', "Processing XML for Teachers        ", end='')
            for d in child:
                i += 1
                print('\b\b\b\b\b', str(i).rjust(4), end='')
                teacher = Teacher()
                teacher.name = d.get("name").strip()
                teacher.short = d.get("short").strip()
                teacher.gender = d.get("gender").strip()
                teacher.color = d.get("color").strip()
                teacher.timetable_id = Timetable.objects.get(pk=tt_id)
                teacher.sort = int(d.get("id").strip()[1:])
                teacher.save()
                id = teacher.id
                teacher_ident[id] = d.get("id").strip()

        elif child.tag == "classes":
            i = 0
            print('\n', "Processing XML for Classes         ", end='')
            for d in child:
                i += 1
                print('\b\b\b\b\b', str(i).rjust(4), end='')
                clas = Class()
                clas.name = d.get("name").strip()
                clas.short = d.get("short").strip()
                clas.timetable_id = Timetable.objects.get(pk=tt_id)
                clas.sort = int(d.get("id").strip()[1:])
                clas.save()
                id = clas.id

                class_ident[id] = d.get("id").strip()

                class_classroomids[id] = d.get("classroomids").strip()
                # clas.classrooms = []
                clrms = class_classroomids[id].split(',')
                classrooms = Classroom.objects.filter(timetable_id=tt_id)
                for clrm in clrms:
                    for classroom in classrooms:
                        id_clr = classroom.id
                        if classroom_ident[id_clr] == clrm:
                            clas.classrooms.add(clrm)

                class_teacherid[id] = d.get("teacherid").strip()
                # clas.teachers = []
                tchs = class_teacherid[id].split(',')
                teachers = Teacher.objects.filter(timetable_id=tt_id)
                for tch in tchs:
                    for teacher in teachers:
                        id_t = teacher.id
                        if teacher_ident[id_t] == tch:
                            clas.teachers.add(tch)

                clas.save()
        elif child.tag == "subjects":
            i = 0
            print('\n', "Processing XML for Subjects        ", end='')
            for d in child:
                i += 1
                print('\b\b\b\b\b', str(i).rjust(4), end='')
                subject = Subject()
                subject.name = d.get("name").strip()
                subject.short = d.get("short").strip()
                subject.timetable_id = Timetable.objects.get(pk=tt_id)
                subject.sort = int(d.get("id").strip()[1:])
                subject.save()
                id = subject.id
                subject_ident[id] = d.get("id").strip()

        elif child.tag == "classrooms":
            i = 0
            print('\n', "Processing XML for Classrooms      ", end='')
            for d in child:
                i += 1
                print('\b\b\b\b\b', str(i).rjust(4), end='')
                classroom = Classroom()
                classroom.name = d.get("name").strip()
                classroom.short = d.get("short").strip()
                classroom.timetable_id = Timetable.objects.get(pk=tt_id)
                classroom.sort = int(d.get("id").strip()[1:])
                classroom.save()
                id = classroom.id
                classroom_ident[id] = d.get("id").strip()

        elif child.tag == "groups":
            i = 0
            print('\n', "Processing XML for Groups          ", end='')
            for d in child:
                i += 1
                print('\b\b\b\b\b', str(i).rjust(4), end='')
                group = Group()
                group.name = d.get("name").strip()
                group.entireclass = d.get("entireclass").strip()
                group.divisiontag = d.get("divisiontag").strip()
                group.studentcount = d.get("studentcount").strip()
                group.timetable_id = Timetable.objects.get(pk=tt_id)
                group.sort = int(d.get("id").strip()[1:])
                group.save()
                id = group.id
                group_ident[id] = d.get("id").strip()

                group_classid[id] = d.get("classid").strip()
                # group.classes = []

                # clases = group_classid[id].split(',')
                # classses = Class.objects.filter(timetable_id=tt_id)
                # for clase in clases:
                #     for classs in classses:
                #         id_clr = classs.id
                #         if class_ident[id_clr] == clase:
                #             group.classrooms.add(clase)
                group.save()


        elif child.tag == "lessons":

            i = 0
            print('\n',"Processing XML for Lessons         ", end='')
            for d in child:
                i += 1
                print('\b\b\b\b\b', str(i).rjust(4), end='')
                lesson = Lesson()
                lesson.periodspercard = d.get("periodspercard").strip()
                lesson.periodsperweek = d.get("periodsperweek").strip()
                lesson.weeks = d.get("weeks").strip()
                lesson.timetable_id = Timetable.objects.get(pk=tt_id)
                lesson.sort = int(d.get("id").strip()[1:])
                lesson.save()
                id = lesson.id
                lesson_ident[id] = d.get("id").strip()

                lesson_subjectid[id] = d.get("subjectid").strip()
                # lesson.subjects = []
                subs = lesson_subjectid[id].split(',')
                subjects = Subject.objects.filter(timetable_id=tt_id)
                for sub in subs:
                    for subject in subjects:
                        id_clr = subject.id
                        if subject_ident[id_clr] == sub:
                            lesson.subjects.add(subject)

                lesson_classids[id] = d.get("classids").strip()
                # lesson.classes = []
                clss = lesson_classids[id].split(',')
                classes = Class.objects.filter(timetable_id=tt_id)
                for cls_ in clss:
                    for classe in classes:
                        id_clr = classe.id
                        if class_ident[id_clr] == cls_:
                            lesson.classes.add(classe)

                lesson_groupids[id] = d.get("groupids").strip()
                # lesson.groups = []
                grs = lesson_groupids[id].split(',')
                groups = Group.objects.filter(timetable_id=tt_id)
                for gr in grs:
                    for group in groups:
                        id_clr = group.id
                        if group_ident[id_clr] == gr:
                            lesson.groups.add(group)


                lesson_studentids[id] = d.get("studentids").strip()


                lesson_teacherids[id] = d.get("teacherids").strip()
                # lesson.teachers = []
                tchs = lesson_teacherids[id].split(',')
                teachers = Teacher.objects.filter(timetable_id=tt_id)
                for tch in tchs:
                    for teacher in teachers:
                        id_clr = teacher.id
                        if teacher_ident[id_clr] == tch:
                            lesson.teachers.add(teacher)


                lesson_classroomids[id] = d.get("classroomids").strip()
                # lesson.classrooms = []
                clrms = lesson_classroomids[id].split(',')
                classrooms = Classroom.objects.filter(timetable_id=tt_id)
                for clrm in clrms:
                    for classroom in classrooms:
                        id_clr = classroom.id
                        if classroom_ident[id_clr] == clrm:
                            lesson.classrooms.add(classroom)


                lesson.save()

        elif child.tag == "cards":
            i = 0
            print('\n', "Processing XML for Cards           ", end='')
            for d in child:
                i += 1
                print('\b\b\b\b\b', str(i).rjust(4), end='')
                # print("")
                card = Card()
                lessonid = d.get("lessonid").strip()
                lessons = Lesson.objects.filter(timetable_id=tt_id)
                for lesson in lessons:
                    if lesson_ident[lesson.id] == lessonid:
                        card.lesson_id = lesson
                day = d.get("day").strip()
                days = Day.objects.filter(timetable_id=tt_id)
                for day_ in days:
                    if day == day_.day:
                        card.day_id = day_
                period = d.get("period").strip()
                period_s = Period.objects.filter(timetable_id=tt_id)
                for period_ in period_s:
                    if period == period_.period:
                        card.period_id = period_



                classroomids = d.get("classroomids").strip()
                card.timetable_id = Timetable.objects.get(pk=tt_id)
                card.save()
                # card.classrooms = []
                clrms = classroomids.split(',')
                clasrooms = Classroom.objects.filter(timetable_id=tt_id)
                for clrm in clrms:
                    for clasroom in clasrooms:
                        id_clr = clasroom.id
                        if classroom_ident[id_clr] == clrm:
                            card.classrooms.add(clasroom)
                card.save()

    print("")
    print("Генеруємо посилання на картки в таблиці вчителів")
    print('\n', "Processing links for Cards         ", end='')
    i = 0
    cards = Card.objects.filter(timetable_id=tt_id)
    for card in cards:
        i += 1
        print('\b\b\b\b\b', str(i).rjust(4), end='')
        if card.lesson_id != None:
            teachers = card.lesson_id.teachers.all()
            for teach in teachers:
                teach.cards.add(card)
    print("")
    p = Settings.objects.filter(field='timetable')[0]
    p.value = str(tt_id)
    p.save()
    # ts = Teacher.objects.filter(timetable_id=tt_id)
    # for t in ts:
    #     cs = Card.objects.filter(timetable_id=tt_id)
    #     for c in cs:
    #         if c.lesson_id != None:
    #             teachers = c.lesson_id.teachers.all()
    #             for teach in teachers:
    #                 if t == teach:
    #                     t.cards.add(c)
    #     t.save()

    print("Завершено")



