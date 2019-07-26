import datetime

from django.shortcuts import render

from worktime.forms import SettingsForm, VacationForm
from worktime.models import Settings, Academyear, Vacat


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
