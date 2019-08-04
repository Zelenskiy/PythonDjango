import datetime
from datetime import timedelta
from distutils.command import register

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView
from django_extensions.db.fields import json

from timetable.models import Teacher, Timetable
from worktime.forms import SettingsForm, VacationForm,  MissForm
from worktime.models import Settings, Academyear, Vacat, Workday, Worktimetable, Missing


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
    success_url = 'worktime/replace.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        st = Settings.objects.filter(field='timetable')[0].value
        tt = Timetable.objects.get(pk=st)
        context['teachers'] = Teacher.objects.filter(timetable_id=tt)
        return context


# def replace(request):
#     st = Settings.objects.filter(field='timetable')[0].value
#     tt = Timetable.objects.get(pk=st)
#     # TODO
#     ac = Academyear.objects.get(pk=1)
#     wt = Worktimetable.objects.filter(acyear_id=ac)[0]
#     teachers = Teacher.objects.filter(timetable_id=tt)
#     missing = Missing.objects.filter(worktimeable=wt)
#
#     # print(teachers[0].name)
#
#
#     context = {'teachers':teachers, 'missing': missing}
#     return render(request, 'worktime/replace.html', context)


@csrf_exempt
def repladd(request):
    if request.POST and request.is_ajax(): # and request.user.has_perm('plan.change_plan'):
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
