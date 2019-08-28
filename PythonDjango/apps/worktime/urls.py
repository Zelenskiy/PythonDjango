
from django.conf.urls import url
from django.conf.urls.static import static
from django.urls import path
from PythonDjango import settings



#
#
from timetable.views import importasc, importgo, viewteachers
from worktime.views import setting, vacation, index, generatewd, setchzn, repladd, MissCreateView, \
    repltable, repldel, replgen, repldel, datesave, resp, pzdel, \
    expnavforcheck, repl_3, HourlyCreateView, exptarif, prepeduplan, hwtable, expfortab, calplandates

urlpatterns = [

                  path('settings/', setting, name='settings_url'),
                  path('vacations/', vacation, name='vacation_url'),
                  path('replace/', MissCreateView.as_view(), name='replace_url'),
                  path('setforpz/', HourlyCreateView.as_view(), name='setforpz_url'),
                  # path('replace/', replace, name='replace_url'),
                  path('repladd/', repladd, name='repladd_url'),
                  path('index/', index, name='index_url'),
                  # path('getmonth/<int:m>/', getmonth, name='getmonth_url'),
                  path('generatewd/', generatewd, name='generatewd_url'),
                  path('setchzn/<int:id>/<int:chzn>/', setchzn, name='setchzn_url'),
                  path('repltable/', repltable, name='repltable_url'),
                  path('hwtable/', hwtable, name='hwtable_url'),
                  path('repldel/<int:id>/', repldel, name='repldel_url'),
                  path('pzdel/<int:id>/', pzdel, name='pzdel_url'),
                  path('replgen/', replgen, name='replgen_url'),
                  path('repldel/', repldel, name='repldel_url'),
                  path('datesave/', datesave, name='datesave_url'),
                  path('resp/', resp, name='resp_url'),
                  path('repl_3/', repl_3, name='repl_3_url'),
                  path('exptarif/', exptarif, name='exptarif_url'),
                  path('expfortab/', expfortab, name='expfortab_url'),
                  path('expnavforcheck/', expnavforcheck, name='expnavforcheck_url'),
                  path('calplandates/', calplandates, name='calplandates_url'),
                  path('prepeduplan/', prepeduplan, name='prepeduplan_url'),



              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
