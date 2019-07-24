from django.shortcuts import render

from worktime.forms import SettingsForm
from worktime.models import Settings


def setting(request):
    settings = Settings.objects.all()
    form = SettingsForm()
    if request.POST:
        print("11111111111")
        kr = ['timetable', 'plantable']
        for set in settings:
            # s = request.POST[set.field]
            f = str(request.POST['field_' + set.field]).strip()
            v = str(request.POST[set.field]).strip()
            for x in kr:
                if (set.field == x) and (f == x):
                    set.value = v
            set.save()
            print("Збережено ")
    context = {'form': form, 'settings': settings}
    return render(request, 'worktime/settings.html', context)
