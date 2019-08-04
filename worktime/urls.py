
from django.conf.urls import url
from django.conf.urls.static import static
from django.urls import path
from PythonDjango import settings



#
#
from timetable.views import importasc, importgo, viewteachers
from worktime.views import setting, vacation, index, generatewd, setchzn, repladd, MissCreateView, repltable, repldel

urlpatterns = [

                  path('settings/', setting, name='settings_url'),
                  path('vacations/', vacation, name='vacation_url'),
                  path('replace/', MissCreateView.as_view(), name='replace_url'),
                  # path('replace/', replace, name='replace_url'),
                  path('repladd/', repladd, name='repladd_url'),
                  path('index/', index, name='index_url'),
                  # path('getmonth/<int:m>/', getmonth, name='getmonth_url'),
                  path('generatewd/', generatewd, name='generatewd_url'),
                  path('setchzn/<int:id>/<int:chzn>/', setchzn, name='setchzn_url'),
                  path('repltable/', repltable, name='repltable_url'),
                  path('repldel/<int:id>/', repldel, name='repldel_url'),



              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
