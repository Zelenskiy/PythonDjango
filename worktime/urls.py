
from django.conf.urls import url
from django.conf.urls.static import static
from django.urls import path
from PythonDjango import settings

from plan.views import index, imp_from_excel, view, postr,  \
    update_plan, Post_delete

#
#
from timetable.views import importasc, importgo, viewteachers
from worktime.views import setting

urlpatterns = [

                  path('settings/', setting, name='settings_url'),


              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
