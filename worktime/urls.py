
from django.conf.urls import url
from django.conf.urls.static import static
from django.urls import path
from PythonDjango import settings



#
#
from timetable.views import importasc, importgo, viewteachers
from worktime.views import setting, vacation, index, generatewd,setchzn

urlpatterns = [

                  path('settings/', setting, name='settings_url'),
                  path('vacations/', vacation, name='vacation_url'),
                  path('index/', index, name='index_url'),
                  # path('getmonth/<int:m>/', getmonth, name='getmonth_url'),
                  path('generatewd/', generatewd, name='generatewd_url'),
                  path('setchzn/<int:id>/<int:chzn>/', setchzn, name='setchzn_url'),


              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
