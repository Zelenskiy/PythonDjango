import datetime
import os
from datetime import timedelta

import openpyxl
from django.core.files.storage import FileSystemStorage

from django.db.models import Q
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView

from PythonDjango.settings import BASE_DIR, MEDIA_DIR
from timetable.models import Teacher, Timetable, Day, Card, Lesson, Subject, Resp
from worktime.forms import SettingsForm, VacationForm, MissForm
from worktime.models import Settings, Academyear, Vacat, Workday, Worktimetable, Missing, Historyrepl


def str_to_datestr(ss1):
    mapping = [' ', ',', '.', '/', '-', '+', '*']
    for v in mapping:
        ss1 = ss1.replace(v, '.')
    ss1 = ss1.strip('.')
    while ss1.find('..') > -1:
        ss1 = ss1.replace('..', '.')
    n = ss1.count('.')
    if n == 1:
        ss1 = ss1 + '.' + str(datetime.datetime.today().year)
    return ss1


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days + 1)):
        yield start_date + timedelta(n)


def generatewd(request):
    ay = Settings.objects.filter(field='academic_year')[0].value.strip()
    workdays = Workday.objects.filter(acyear_id__name__iexact=ay)
    vacations = Vacat.objects.filter(acyear_id__name__iexact=ay, deleted=False)
    start = Settings.objects.filter(field='startacyear')[0].value.strip()
    end = Settings.objects.filter(field='endacyear')[0].value.strip()
    if request.POST:
        # вилучаємо робочі дні за поточний навчальний рік
        Workday.objects.filter(acyear_id__name__iexact=ay).delete()
        # Формуємо нову таблицю робочих днів
        d1 = datetime.datetime.strptime(start, '%d.%m.%Y')
        d2 = datetime.datetime.strptime(end, '%d.%m.%Y')
        i = 0
        nw = 1
        n0 = 0
        for d in daterange(d1, d2):
            # print (d.strftime("%Y-%m-%d"))
            day = Workday()
            day.wday = d
            # Перевіряємо в таблиці Vacat
            count = len(Vacat.objects.filter(date=d))
            if count == 0:
                d_week = d.weekday() + 1
                day.dayweek = d_week
            else:
                d_week = 6
                day.dayweek = d.weekday() + 1

            if d_week == 6:
                day.numworkweek = 0
                day.num = 0
                day.weekchzn = 0
            elif d_week == 7:
                day.numworkweek = 0
                day.num = 0
                day.weekchzn = 0
                n0 = 1
            else:
                if n0 == 1:
                    nw += 1
                    n0 = 0
                day.numworkweek = nw
                i += 1
                day.num = i
                day.weekchzn = (nw + 1) % 2 + 1

                day.worktimetable_id = Worktimetable.objects.get(pk=1)

            day.acyear_id = Academyear.objects.get(pk=Vacat.objects.filter(acyear_id__name__iexact=ay)[0].id)
            day.save()
        ay = Settings.objects.filter(field='academic_year')[0].value.strip()
        workdays = Workday.objects.filter(acyear_id__name__iexact=ay)

    context = {'workdays': workdays, 'vacations': vacations, 'year': ay, 'start': start, 'end': end}
    return render(request, 'worktime/generatewd.html', context)


def index(request):
    ay = Settings.objects.filter(field='academic_year')[0].value.strip()
    workdays = Workday.objects.filter(acyear_id__name__iexact=ay)
    start = Settings.objects.filter(field='startacyear')[0].value.strip()
    end = Settings.objects.filter(field='endacyear')[0].value.strip()
    # vacations = Vacat.objects.filter(acyear_id__name__iexact=ay, deleted=False)
    if request.POST:
        for workday in workdays:
            s = request.POST['i-' + str(workday.id)]
            id_i = int(s)
            flag = False
            w = Workday.objects.get(pk=id_i)
            if (w.num != int(request.POST['n-' + s])):
                w.num = int(request.POST['n-' + s])
                flag = True
            dat_form = request.POST['w-' + s]
            dat_model = w.wday.strftime("%d.%m.%Y")

            if dat_model != dat_form:
                w.wday = datetime.datetime.strptime(request.POST['w-' + s], '%d.%m.%Y')
                flag = True
            if (w.numworkweek != int(request.POST['u-' + s])):
                w.numworkweek = int(request.POST['u-' + s])
                flag = True
            if (w.dayweek != int(request.POST['d-' + s])):
                w.dayweek = int(request.POST['d-' + s])
                flag = True
            if (w.weekchzn != int(request.POST['e-' + s])):
                w.weekchzn = int(request.POST['e-' + s])
                flag = True
            if flag:
                w.save()
                print("Збережено")
    # print(len(workdays))

    context = {'workdays': workdays, 'year': ay, 'start': start, 'end': end}

    return render(request, 'worktime/index.html', context)


class MissCreateView(CreateView):
    template_name = 'worktime/replace.html'
    form_class = MissForm
    success_url = '../../worktime/replace/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # ac = Academyear.objects.get(pk=1)
        # wt = Worktimetable.objects.filter(acyear_id=ac)[0]

        # context['worktimeable'] = (wt)

        st = Settings.objects.filter(field='histreplst')[0].value.strip()
        fin = Settings.objects.filter(field='histreplfin')[0].value.strip()
        sthist = Settings.objects.filter(field='histzamst')[0].value.strip()
        finhist = Settings.objects.filter(field='histzamfin')[0].value.strip()
        fileHist = Settings.objects.filter(field='fileHist')[0].value.strip()
        context['st'] = st
        context['fin'] = fin
        context['sthist'] = sthist
        context['finhist'] = finhist
        context['fileHist'] = fileHist
        return context

    def form_valid(self, form):
        ac = Academyear.objects.get(pk=1)
        # wt = Worktimetable.objects.filter(acyear_id=ac)[0]

        ttfrset = Settings.objects.filter(field='worktimetable')[0].value
        wt = Worktimetable.objects.get(pk=int(ttfrset))
        form.instance.worktimeable = wt
        return super(MissCreateView, self).form_valid(form)

    def form_invalid(self, form):
        print("invalid")
        return super(MissCreateView, self).form_invalid(form)


def psmaker(filename, d1, d2):
    wb = openpyxl.load_workbook(os.path.join(BASE_DIR, 'media', filename))
    sheet = wb['Аркуш1']
    # Рахуємо кількість заповнених рядків у таблиці Excel. У n номер останнього рядка з даними
    n = 1
    k = 1
    s = str(sheet['A' + str(n)].value)
    history = []
    while s is not None:
        rec = {}
        n += 1
        s = str(sheet['A' + str(n)].value)
        dat = (sheet['B' + str(n)].value)
        # dat = datetime.datetime.strptime(datS,'%Y-%m-%d %h:%m:%s')

        try:
            k = int(s)
        except:
            break
        if (dat > d1 or dat == d1) and (dat < d2 or dat == d2):
            rec['D'] = dat

            rec['VT'] = str(sheet['C' + str(n)].value)
            rec['PV'] = str(sheet['D' + str(n)].value)
            rec['P1'] = str(sheet['E' + str(n)].value)
            rec['KL'] = str(sheet['F' + str(n)].value)
            rec['ZT'] = str(sheet['G' + str(n)].value)
            rec['P2'] = str(sheet['I' + str(n)].value)
            tmp = str(sheet['J' + str(n)].value)
            if tmp == 'pk':
                rec['poch_kl'] = True
            else:
                rec['poch_kl'] = False
            history += [rec]
    print(n)
    # D_old = datetime.datetime.strptime('01.09.2000', '%d.%m.%Y')
    # VT_old = ''
    # PV_old = ''
    # P1_old = ''
    # KL_old = ''
    # ZT_old = ''
    # P2_old = ''
    # poch_kl_old = False
    teachers = []
    for h in history:
        # Визначаємо кількість вчителів
        title = h['VT'] + '~' + h['PV']
        reason = h['PV']
        # rec = {}
        if not title in teachers:
            teach = h['VT']
            subjects = []
            zamteachers = []
            rec = {}
            for h2 in history:
                title2 = h2['VT'] + '~' + h2['PV']
                if title == title2:
                    #--------------------------
                    zam = h2['ZT']
                    if not zam in zamteachers:
                        zamsubjects = []
                        for h3 in history:
                            title3 = h3['VT'] + '~' + h3['PV']
                            if title2 == title3 and h3['ZT'] == zam:
                                subject = h3['P1']
                                if not subject in zamsubjects:
                                    klases = []
                                    for h4 in history:
                                        title4 = h4['VT'] + '~' + h4['PV']
                                        if title3 == title4 and h4['P1'] == h3['P1']:
                                            klas = h4['KL']
                                            if not klas in klases:
                                                klases += [klas]
                                    rec2 = {}

                                    rec2['subject'] = subject
                                    rec2['classes'] = klases
                                    if not rec2 in subjects:
                                        subjects += [rec2]
                                rec4 = {}
                                rec4 ['zteach'] = zam
                                rec4['subj'] = subjects
                        zamteachers += [rec4]
                    rec3 = {}
                    rec3['subjects'] = zamteachers

                    #-------------------------------------------------
                    subject = h2['P1']
                    if not subject in subjects:
                        klases = []
                        for h3 in history:
                            title3 = h3['VT'] + '~' + h3['PV']
                            if title2 == title3 and h3['P1'] == h2['P1']:
                                klas = h3['KL']
                                if not klas in klases:
                                    klases += [klas]
                        rec1 = {}
                        rec1['subject'] = subject
                        rec1['classes'] = klases
                        if not rec1 in subjects:
                            subjects += [rec1]


            rec['title'] = title
            rec['reason'] = reason
            rec['subjects'] = subjects
            rec['teach'] = teach
            rec['zamteach'] = [rec3]
            if not rec in teachers:
                teachers += [rec]

    for t in teachers:
        count = 0
        date = []
        dss = []

        for h in history:
            title = h['VT'] + '~' + h['PV']

            if title == t['title']:
                count += 1
                ds = date_to_dd_mm(h['D'])
                if not ds in dss:
                    dss += [ds]
                date += [ds]
                # Вчителі, що заміняють
                # z = h['ZT']
                # if not z in zamt:
                #     zamt += [z]

        t['count'] = count
        # t['date'] = date
        t['min'] = min_list(date)
        t['max'] = max_list(date)
        t['days'] = len(dss)
        # t['zamt'] = zamt

    listExcel = []

    for i, t in enumerate(teachers):
        rec = {}
        rec['N'] = str(i + 1)
        rec['teach'] = t['teach']
        subjects = t['subjects']
        s = ''
        for subject in subjects:
            klss = ''
            for kl in subject['classes']:
                klss += kl
            klss = klss.replace('-', '')
            s += subject['subject'] + '(' + klss + '),'
        rec['subject'] = s[:-1]
        rec['dmin'] = t['min']
        rec['dmax'] = t['max']
        rec['days'] = t['days']
        rec['count'] = t['count']
        rec['reason'] = t['reason']

        listExcel += [rec]

    wb = openpyxl.load_workbook(os.path.join(BASE_DIR, 'media', 'templ', 'PZap.xlsx'))
    sheet = wb['Аркуш1']

    n = 7
    for t in listExcel:
        sheet['B' + str(n)].value = t['N']
        sheet['C' + str(n)].value = t['teach']
        sheet['D' + str(n)].value = t['subject']
        sheet['E' + str(n)].value = t['dmin']
        sheet['F' + str(n)].value = t['dmax']
        sheet['G' + str(n)].value = t['days']
        sheet['H' + str(n)].value = t['count']
        sheet['L' + str(n)].value = t['reason']

        n += 2

    wb.save(os.path.join(BASE_DIR, 'media', 'report', 'PZap.xlsx'))


    # for t in teachers:
    #
    #     for h in history:
    #         title = h['VT'] + '~' + h['PV']
    #         z = h['ZT']
    #         subjects = []
    #
    #         for h2 in history:
    #             title2 = h2['VT'] + '~' + h2['PV']
    #             if title == title2 and z == h2['ZT'] :
    #                 subject = h2['P1']
    #                 if not subject in subjects:
    #                     klases = []
    #                     for h3 in history:
    #                         title3 = h3['VT'] + '~' + h3['PV']
    #                         if title2 == title3 and z == h2['ZT'] and h3['P1'] == h2['P1']:
    #                             klas = h3['KL']
    #                             if not klas in klases:
    #                                 klases += [klas]
    #                     rec1 = {}
    #                     rec1[subject] = klases
    #                     if not rec1 in subjects:
    #                         subjects += [rec1]
    #         rec = {}
    #         rec[h2['ZT']] = subjects
    #         if not rec in zamt:
    #             zamt += [rec]
    #     t['zamt'] = zamt


def min_list(ls):
    min = ls[0]
    for l in ls:
        if l < min:
            min = l
    return min


def max_list(ls):
    max = ls[0]
    for l in ls:
        if l > max:
            max = l
    return max


def date_to_dd_mm(d):
    day = '0' + str(d.day)[-2:]
    month = '0' + str(d.month)[-2:]
    return day + '.' + month + '.'


@csrf_exempt
def repl_3(request):
    if request.method == 'POST' and request.FILES['upload']:
        myfile = request.FILES['upload']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        s1 = request.POST['datepicker5']
        s2 = request.POST['datepicker6']
        d1 = datetime.datetime.strptime(s1, '%d.%m.%Y')
        d2 = datetime.datetime.strptime(s2, '%d.%m.%Y')

        psmaker(filename, d1, d2)
        # print('filename='+filename)
        # print('uploaded_file_url='+uploaded_file_url)

    context = {}
    return render(request, 'worktime/replace.html', context)


@csrf_exempt
def datesave(request):
    if request.POST and request.is_ajax():
        d1 = request.POST['datepicker3']
        d2 = request.POST['datepicker4']
        s = Settings.objects.filter(field='histreplst')[0]
        s.value = d1
        s.save()
        s = Settings.objects.filter(field='histreplfin')[0]
        s.value = d2
        s.save()
    return render(request, 'worktime/replace.html', {})


@csrf_exempt
def repldel(request, id):
    if request.POST and request.is_ajax():
        Missing.objects.get(pk=id).delete()
    return render(request, 'worktime/replace.html', {})


@csrf_exempt
def replgen(request):
    context = {}
    if request.POST and request.is_ajax():
        # s1 = request.POST['datepicker3']  # 01.09.2019
        # s2 = request.POST['datepicker4']
        #
        # y1 = int(s1[6:])
        # y2 = int(s2[6:])
        # m1 = int(s1[3:5])
        # m2 = int(s2[3:5])
        # D1 = int(s1[:2])
        # D2 = int(s2[:2])
        # d1 = datetime.datetime(y1, m1, D1, 1, 1, 1, 1, tzinfo=pytz.UTC)
        # d2 = datetime.datetime(y2, m2, D2, 1, 1, 1, 1, tzinfo=pytz.UTC)
        d1 = datetime.datetime.strptime(request.POST['datepicker3'], '%d.%m.%Y')
        d2 = datetime.datetime.strptime(request.POST['datepicker4'], '%d.%m.%Y')

        # TODO
        ac = Academyear.objects.get(pk=1)
        # wt = Worktimetable.objects.filter(acyear_id=ac)[0]

        ttfrset = Settings.objects.filter(field='worktimetable')[0].value
        wt = Worktimetable.objects.get(pk=int(ttfrset))
        ttfrset = Settings.objects.filter(field='timetable')[0].value
        tt = Timetable.objects.get(pk=int(ttfrset))
        text = ''
        for d in daterange(d1, d2):
            wdays = Workday.objects.filter(worktimetable=wt, wday=d)
            if len(wdays) < 1:
                continue
            wday = wdays[0]
            wdweek = wday.weekchzn  # Ціле число "1-чис., 2-зн., 0-вихідний"
            if wdweek == 1:
                wdw = '10'
            elif wdweek == 2:
                wdw = '01'
            else:
                continue
            # День тижня
            dayofweek = wday.dayweek - 1
            q = Q(worktimeable=wt) & Q(date_st__lte=wday.wday) & Q(date_fin__gte=wday.wday)

            missings = Missing.objects.filter(q)
            day = Day.objects.filter(timetable_id=tt, day=dayofweek)[0]
            if len(missings) > 0:
                for missing in missings:
                    # tchmiss = missing.teach_id
                    teach = Teacher.objects.get(pk=missing.teach_id)
                    if teach != None:
                        cardsinteach = teach.cards.all()
                        # if len(cardsinteach) > 0:
                        for card in cardsinteach:
                            lesson = card.lesson_id
                            if (card.day_id == day) and ((lesson.weeks == '1') or (lesson.weeks == wdw)):
                                sbs = [x.short for x in lesson.subjects.all()]
                                ss = ''.join(sbs)
                                sbs = [x.short for x in lesson.classes.all()]
                                cs = ''.join(sbs)
                                reason = missing.reason
                                if reason == None:
                                    reason = ''
                                if missing.poch_kl:
                                    poch = 'pk'
                                else:
                                    poch = ''
                                periodsprcard = int(lesson.periodspercard)
                                for psc in range(periodsprcard):
                                    print(teach.short, "\t", d, "\t", ss, "\t", cs, "\t", reason)
                                    text += '\n\t' + d.strftime(
                                        "%d.%m.%y") + "\t" + teach.short + "\t" + reason + "\t" + ss + \
                                            "\t" + cs + "\t" + "\t" + "\t" + ss + "\t" + poch + "\t"
        resp = Resp()
        resp.timetable_id = tt
        resp.text = text
        resp.save()

        # Відпраляємо відповідь назад
        context = {}
    return render(request, 'worktime/replace.html', context)


def resp(request):
    ttfrset = Settings.objects.filter(field='timetable')[0].value
    tt = Timetable.objects.get(pk=int(ttfrset))
    r = Resp.objects.filter(timetable_id=tt)
    if len(r) > 0:
        context = {'resp': r[0].text[1:]}
    else:
        context = {}
    return render(request, 'worktime/resp.html', context)


def repltable(request):
    # TODO
    ac = Academyear.objects.get(pk=1)
    # wt = Worktimetable.objects.filter(acyear_id=ac)[0]

    ttfrset = Settings.objects.filter(field='worktimetable')[0].value
    wt = Worktimetable.objects.get(pk=int(ttfrset))
    # ttfrset = Settings.objects.filter(field='timetable')[0].value
    # tt = Timetable.objects.get(pk=int(ttfrset))

    missing = Missing.objects.filter(worktimeable=wt)

    context = {'missing': missing}
    return render(request, 'worktime/repltable.html', context)


@csrf_exempt
def repladd(request):
    if request.POST and request.is_ajax():  # and request.user.has_perm('plan.change_plan'):
        r = Missing()

        # TODO виправити хрінь з цією табл
        r.worktimeable = Worktimetable.objects.get(pg=1)
        r.date_st = datetime.datetime.strptime(request.POST['datepicker1'], '%d.%m.%Y')
        r.date_fin = datetime.datetime.strptime(request.POST['datepicker2'], '%d.%m.%Y')
        r.reason = request.POST['reason']
        st = Settings.objects.filter(field='timetable')[0].value
        tt = Timetable.objects.get(pk=st)
        teachers = Teacher.objects.filter(timetable_id=tt)
        for teacher in teachers:
            pass

    return render(request, 'worktime/replace.html')


@csrf_exempt
def setchzn(request, id, chzn):
    workday = Workday.objects.get(pk=id)
    workday.weekchzn = chzn
    workday.save()
    return render(request, 'worktime/index.html')


def vacation(request):
    flag = 0
    form = VacationForm()
    ay = Settings.objects.filter(field='academic_year')[0].value.strip()
    vacations = Vacat.objects.filter(acyear_id__name__iexact=ay, deleted=False)
    if request.POST:
        flag = 1
        for vac in vacations:
            s = request.POST['n_' + str(vac.id)]
            # існуючий запис
            id_i = int(s)
            v = Vacat.objects.get(pk=id_i)
            v.date = datetime.datetime.strptime(request.POST['dat_' + s], '%d.%m.%Y')
            v.name = request.POST['nam_' + s]
            if request.POST.get('del_' + s, False):
                v.deleted = True
            v.save()
        # додаємо нові
        for n in range(1, 5):
            ss1 = request.POST.get('dat-' + str(n), '')
            ss2 = request.POST.get('nam-' + str(n), '')
            if ss1 != '' and ss2 != '':
                v = Vacat()
                v.name = ss2
                ss1 = str_to_datestr(ss1)
                try:
                    v.date = datetime.datetime.strptime(ss1, '%d.%m.%Y')
                except:
                    try:
                        v.date = datetime.datetime.strptime(ss1, '%d.%m.%y')
                    except:
                        print("Формат дати невірний")

                v.acyear_id = Academyear.objects.get(pk=Vacat.objects.filter(acyear_id__name__iexact=ay)[0].id)
                v.save()
        ay = Settings.objects.filter(field='academic_year')[0].value.strip()
        vacations = Vacat.objects.filter(acyear_id__name__iexact=ay, deleted=False)
        Vacat.objects.filter(deleted=True).delete()

    context = {'vacations': vacations, 'form': form, 'flag': flag}
    return render(request, 'worktime/vacations.html', context)


def setting(request):
    settings = Settings.objects.all()
    kr = []
    flag = 0
    for set in settings:
        kr.append(set.field)
    form = SettingsForm()
    if request.POST:
        flag = 1
        for set in settings:
            f = str(request.POST['field_' + set.field]).strip()
            v = str(request.POST[set.field]).strip()
            for x in kr:
                if (set.field == x) and (f == x):
                    set.value = v
            set.save()
            print("Збережено ")
    context = {'form': form, 'settings': settings, 'flag': flag}
    return render(request, 'worktime/settings.html', context)
