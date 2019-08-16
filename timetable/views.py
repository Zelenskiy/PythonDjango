import codecs
import copy
import os
import random

import openpyxl
from django.core.files.storage import FileSystemStorage
from django.db.models import Q
from django.http import FileResponse
from django.shortcuts import render
import xml.etree.ElementTree as ET

from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView

from PythonDjango.settings import BASE_DIR
from timetable.forms import TeacherForm
from timetable.models import *
import logging

from worktime.models import Settings, Missing, Hourlyworker


# logging.basicConfig(filename="log-file.log", level=logging.INFO)


# logging.info("Открыт Каталог товаров")

class TeacherCreateView(CreateView):
    template_name = 'timetable/teachers.html'
    form_class = TeacherForm
    success_url = '../../timetable/teachers/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ttfrset = Settings.objects.filter(field='timetable')[0].value
        tt = Timetable.objects.get(pk=int(ttfrset))
        context['teachers'] = Teacher.objects.filter(timetable_id=tt)

        return context

    def form_valid(self, form):
        ttfrset = Settings.objects.filter(field='timetable')[0].value
        tt = Timetable.objects.get(pk=int(ttfrset))

        form.instance.timetable_id = tt
        return super(TeacherCreateView, self).form_valid(form)

    def form_invalid(self, form):
        print("invalid")
        return super(TeacherCreateView, self).form_invalid(form)


@csrf_exempt
def tchdel(request, id):
    if request.POST and request.is_ajax():
        Teacher.objects.get(pk=id).delete()
    return render(request, 'timetable/teachers.html', {})


def expeduplan(request):

    if request.method == 'POST' and request.FILES['myfile']:
        filename_out = os.path.join(BASE_DIR, 'media', 'report', 'workload.xml')

        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename_in = fs.save(myfile.name, myfile)

        # filename_in = 'D:/MyDoc/PythonDjango/ENav0.xlsx'
        # filename_in = os.path.join(BASE_DIR, 'media', 'templ', 'ENav.xlsx')
        wb = openpyxl.load_workbook(filename_in)
        sheet = wb['Навантаження']
        # Рахуємо кількість заповнених рядків у таблиці Excel. У n номер останнього рядка з даними
        n = 2
        k = 1

        lessons = []
        teachers = []
        classes = []
        classrooms = []
        subjects = []
        n = 2
        while True:
            # while s is not None:
            n += 1
            s = str(sheet['B' + str(n)].value).strip()
            if s == 'None':
                break
            rec = {}
            rec['groupids'] = []
            c1 = str(sheet['B' + str(n)].value)
            c2 = str(sheet['C' + str(n)].value)
            c3 = str(sheet['D' + str(n)].value)
            t1 = str(sheet['H' + str(n)].value)
            t2 = str(sheet['I' + str(n)].value)
            t3 = str(sheet['J' + str(n)].value)
            r1 = str(sheet['K' + str(n)].value)
            r2 = str(sheet['L' + str(n)].value)
            r3 = str(sheet['M' + str(n)].value)
            g1 = str(sheet['N' + str(n)].value)
            g2 = str(sheet['O' + str(n)].value)
            g3 = str(sheet['P' + str(n)].value)
            rec['classids'] = [c1]
            if str(c2) != 'None':
                rec['classids'] += [c2]
            if str(c3) != 'None':
                rec['classids'] += [c3]
            rec['subjectid'] = sheet['E' + str(n)].value
            obj_to_list(rec['subjectid'], subjects)
            rec['periodspercard'] = str(sheet['F' + str(n)].value)
            if rec['periodspercard'] == 'None':
                rec['periodspercard'] = '1'
            rec['periodsperweek'] = str(sheet['G' + str(n)].value)
            rec['teacherids'] = [t1]

            if str(t2) != 'None':
                rec['teacherids'] += [t2]
            if str(t3) != 'None':
                rec['teacherids'] += [t3]
            rec['classroomids'] = [r1]
            if str(r2) != 'None':
                rec['classroomids'] += [r2]
            if str(r3) != 'None':
                rec['classroomids'] += [r3]
            if str(g1) == 'None':
                rec['groupids'] = ['']
                if str(g2) != 'None':
                    rec['groupids'] += [g2]
                    if str(g3) != 'None':
                        rec['groupids'] += [g3]
            rec['studentids'] = str(sheet['Q' + str(n)].value)
            if rec['studentids'] == 'None':
                rec['studentids'] = ''
            rec['weeks'] = str(sheet['R' + str(n)].value)
            if rec['weeks'] == 'None':
                rec['weeks'] = '1'
            weektmp = rec['weeks']
            k = rec['periodsperweek'].find('.')
            if k > -1:
                rec['periodsperweek'] = rec['periodsperweek'][:k]
                rec['weeks'] = '1'
                lessons += [rec]
                rec2 = copy.deepcopy(rec)
                rec2['weeks'] = weektmp
                rec2['periodsperweek'] = '0.5'
                lessons += [rec2]
            else:
                lessons += [rec]

            obj_to_list(t1, teachers)
            obj_to_list(t2, teachers)
            obj_to_list(t3, teachers)
            obj_to_list(c1, classes)
            obj_to_list(c2, classes)
            obj_to_list(c3, classes)
            obj_to_list(r1, classrooms)
            obj_to_list(r2, classrooms)
            obj_to_list(r2, classrooms)

        teachers.sort()

        t_list = []
        # id,name,short,gender,color
        for i, t in enumerate(teachers):
            rec = {}
            rec['id'] = '*' + str(i + 1)
            rec['name'] = t
            rec['short'] = namet_to_short(t)
            if t[-2:] == 'ич':
                rec['gender'] = 'M'
            else:
                rec['gender'] = 'F'
            dec = random.randint(1, 16777215)
            rec['color'] = '#' + hex(dec).split('x')[-1].upper()
            t_list += [rec]
        classes.sort()
        c_list = []
        # id,name,short,classroomids,teacherid
        for i, c in enumerate(classes):
            rec = {}
            rec['id'] = '*' + str(i + 1)
            rec['name'] = c
            rec['short'] = c
            rec['classroomids'] = ''
            rec['teacherid'] = ''
            c_list += [rec]
        subjects.sort()
        s_list = []
        # id,name,short
        for i, s in enumerate(subjects):
            rec = {}
            rec['id'] = '*' + str(i + 1)
            rec['name'] = s
            rec['short'] = s
            s_list += [rec]
        classrooms.sort()
        r_list = []
        # id,name,short
        for i, r in enumerate(classrooms):
            rec = {}
            rec['id'] = '*' + str(i + 1)
            rec['name'] = r
            rec['short'] = r
            r_list += [rec]
        g_list = []
        # id,classid,name,entireclass,divisiontag,studentcount
        i = 0
        ngr = ['Весь клас', '1 група', '2 група', 'Хлопці', 'Дівчата']
        for num_cl, c in enumerate(classes):
            for num_gr, g in enumerate(ngr):
                i += 1
                rec = {}
                rec['id'] = '*' + str(i)
                rec['classid'] = '*' + str(num_cl + 1)
                rec['name'] = g
                if num_gr == 0:
                    rec['entireclass'] = '1'
                    rec['divisiontag'] = '0'
                else:
                    rec['entireclass'] = '0'
                    if num_gr == 1 or num_gr == 2:
                        rec['divisiontag'] = '1'
                    else:
                        rec['divisiontag'] = '2'
                rec['studentcount'] = ''
                g_list += [rec]

        # id,subjectid,classids,groupids,studentids,teacherids,classroomids,periodspercard,periodsperweek,weeks
        l_list = []
        for i, l in enumerate(lessons):
            print(i)
            rec = {}
            rec['classids'] = ''
            rec['groupids'] = ''
            rec['teacherids'] = ''
            rec['classroomids'] = ''
            rec['periodspercard'] = l['periodspercard']
            rec['periodsperweek'] = l['periodsperweek']
            rec['weeks'] = l['weeks']
            rec['id'] = '*' + str(i + 1)
            l['groupids'] +=['']+ ['']
            for s in s_list:
                if s['name'] == l['subjectid']:
                    rec['subjectid'] = s['id']
            for cii, cls in enumerate(l['classids']):
                for ci, c in enumerate(c_list):
                    sh = 0
                    # g = l['groupids'][cii]
                    # if g == '':
                    #     sh = 0
                    # else:
                    #     sh = int(g)
                    # print('sh=',sh)
                    if c['name'] == cls:
                        rec['classids'] += c['id'] + ','

                        gr = cl_to_gr(c['id'], sh, c_list, g_list)
                        rec['groupids'] += gr+','


            rec['classids'] = rec['classids'][:-1]
            rec['groupids'] = rec['groupids'][:-1]
            rec['teacherids'] = ''
            for ts in l['teacherids']:
                for t in t_list:
                    if t['name'] == ts:
                        rec['teacherids'] += t['id'] + ','
            rec['teacherids'] = rec['teacherids'][:-1]
            rec['classroomids'] = ''
            for ts in l['classroomids']:
                for t in r_list:
                    if t['name'] == ts:
                        rec['classroomids'] += t['id'] + ','
            rec['classroomids'] = rec['classroomids'][:-1]

            l_list += [rec]

        text = '<timetable importtype="database" options="idprefix:XML,groupstype1,' \
               'decimalseparatordot" defaultexport="1">' + '\n' + \
               '   <days options="canadd" columns="day,name,short">' + '\n' + \
               '     <day name="Понеділок" short="Пн." day="0"/>' + '\n' + \
               '     <day name="Вівторок" short=" Вт." day="1"/>' + '\n' + \
               '     <day name="Середа" short=" Ср." day="2"/>' + '\n' + \
               '     <day name="Четвер" short=" Чт." day="3"/>' + '\n' + \
               '     <day name="П\'ятниця" short="Пт." day="4"/>' + '\n' + \
               '   </days>' + '\n' + \
               '   <periods options="canadd" columns="period,starttime,endtime">' + '\n' + \
               '      <period period="1" starttime="8:30" endtime="9:15"/>' + '\n' + \
               '      <period period="2" starttime="9:25" endtime="10:10"/>' + '\n' + \
               '      <period period="3" starttime="10:30" endtime="11:15"/>' + '\n' + \
               '      <period period="4" starttime="11:35" endtime="12:20"/>' + '\n' + \
               '      <period period="5" starttime="12:30" endtime="13:15"/>' + '\n' + \
               '      <period period="6" starttime="13:25" endtime="14:10"/>' + '\n' + \
               '      <period period="7" starttime="14:20" endtime="15:05"/>' + '\n' + \
               '      <period period="8" starttime="15:15" endtime="16:00"/>' + '\n' + \
               '   </periods>' + '\n' \
                                 '   <teachers options="canadd" columns="id,name,short,gender,color">' + '\n' + \
               '' + '\n'
        for t in t_list:
            text += '      <teacher id="' + t['id'] + '" name="' + t['name'] + \
                    '" short="' + t['short'] + '" gender="' + t[
                'gender'] + '" color="' + t['color'] + '"/>' + '\n'
        text += '   </teachers>' + '\n'
        text += '   <classes options="canadd" columns="id,name,short,classroomids,teacherid">' + '\n'
        for c in c_list:
            text += '      <class id="' + c['id'] + '" name="' + c['name'] + '" short="' + c[
                'short'] + '" teacherid="" classroomids=""/>' + '\n'
        text += '   </classes>' + '\n'
        text += '   <subjects options="canadd" columns="id,name,short">' + '\n'
        for s in s_list:
            text += '      <subject id="' + s['id'] + '" name="' + s['name'] + '" short="' + s['short'] + '"/>' + '\n'
        text += '   </subjects>' + '\n'
        text += '   <classrooms options="canadd" columns="id,name,short">' + '\n'
        for r in r_list:
            text += '      <classroom id="' + r['id'] + '" name="' + r['name'] + '" short="' + r['short'] + '"/>' + '\n'
        text += '   </classrooms>' + '\n'
        text += '   <students options="canadd" columns="id,classid,name"/>' + '\n'
        text += '   <groups options="canadd" columns="id,classid,name,entireclass,divisiontag,studentcount">' + '\n'
        for g in g_list:
            text += '      <group id="' + g['id'] + '" name="' + g['name'] + '" classid="' + g['classid'] + \
                    '" entireclass="' + g['entireclass'] + '" divisiontag="' + \
                    g['divisiontag'] + '" studentcount=""/>' + '\n'
        text += '   </groups>' + '\n'
        text += '   <lessons options="canadd" columns="id,subjectid,classids,groupids,studentids,teacherids,' \
                'classroomids,periodspercard,periodsperweek,weeks">' + '\n'
        for l in l_list:
            text += '      <lesson id="' + l['id'] + '" classids="' + l['classids'] + '" subjectid="' + l[
                'subjectid'] + '" periodspercard="' + l['periodspercard'] + '" ' \
                                                                            'periodsperweek="' + l[
                        'periodsperweek'] + '" teacherids="' + l['teacherids'] + '" classroomids="' + l[
                        'classroomids'] + '" groupids="' + l['groupids'] + '" studentids="" weeks="' + l[
                        'weeks'] + '"/>' + '\n'
        text += '   </lessons>' + '\n'
        text += '   <cards options="canadd" columns="lessonid,day,period,classroomids"/>' + '\n'
        text += '</timetable>' + '\n'

        open(filename_out, "w").write(text)

        return FileResponse(open(filename_out, 'rb'), as_attachment=True)

    else:
        context = {}
        return render(request, 'timetable/importeduplan.html', context)



def cl_to_gr(cl, sh, c_list, g_list):
    c =int(cl[1:])
    g = c * 5 - 5 + 1 + sh
    return '*'+str(g)

def obj_to_list(t, ts):
    if t != 'None':
        if not t in ts:
            ts += [t]


def namet_to_short(name):
    short = name
    ss = name.split()
    if len(ss) == 3:
        short = ss[0] + ' ' + ss[1][:1].upper() + '.' + ss[2][:1].upper() + '.'
    return short


def tchtable(request):
    ttfrset = Settings.objects.filter(field='timetable')[0].value
    tt = Timetable.objects.get(pk=int(ttfrset))
    teachers = Teacher.objects.filter(timetable_id=tt)
    context = {'teachers': teachers}
    return render(request, 'timetable/tchtable.html', context)


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
    # Missing.objects.all().delete()
    # Hourlyworker.objects.all().delete()
    # Card.objects.all().delete()
    # Class.objects.all().delete()
    # Classroom.objects.all().delete()
    # Teacher.objects.all().delete()
    # Day.objects.all().delete()
    # Group.objects.all().delete()
    # Lesson.objects.all().delete()
    # Period.objects.all().delete()
    # Resp.objects.all().delete()
    # Subject.objects.all().delete()
    # Timetable.objects.all().delete()

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

    lesson_subjectid = {}
    lesson_classids = {}
    lesson_groupids = {}
    lesson_studentids = {}
    lesson_teacherids = {}
    lesson_classroomids = {}

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
            print('\n', "Processing XML for Lessons         ", end='')
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
