"""PythonDjango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.conf.urls.static import static
from django.urls import path
from PythonDjango import settings

from plan.views import index, imp_from_excel, view, postr,  \
    update_plan, Post_delete, ribbon, ribbview,rib_update_plan, export_word

#
#


urlpatterns = [
                  # url(r'^rib_update_plan/([0-9]+)/([0-9]{1})/', rib_update_plan, name='rib_update_plan_url'),

                  url(r'^del_plan/([0-9]+)/', Post_delete.as_view()),
                  # url(r'^del_plan/([0-9]+)/', del_plan, name='del_plan'),
                  path('import/', imp_from_excel, name='imp_from_excel'),
                  path('rib_update_plan/<int:id>/<int:num_field>/', rib_update_plan, name='rib_update_plan_url'),
                  path('view/<int:r_id>/<int:num>/', postr, name='postr'),
                  path('ribbon/<int:r_id>/', ribbview, name='ribbview_url'),
                  path('view/', view, name='view'),
                  path('ribbon/', ribbon, name='ribbon_url'),
                  path('export_word/', export_word, name='export_word_url'),
                  path('', index, name='index'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
