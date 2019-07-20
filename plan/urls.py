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
from django.urls import path, include
from PythonDjango import settings

from plan.views import index, imp_from_excel, view, post, postr, add, MyRegisterFormView, PlanEditView, add_ajax, \
    update_plan, add_plan

#
#


urlpatterns = [
                  url(r'^update_plan/([0-9]+)/', update_plan, name='update_plan'),
                  url(r'^add_plan/([0-9]+)/$', add_plan, name='add_plan'),
                  path('import/', imp_from_excel, name='imp_from_excel'),
                  path('add/<int:r_id>/', add, name='add'),
                  path('post/<int:id>/', post, name='post'),

                  # path('view/update_plan/', update_plan),
                  path('view/<pk>/', PlanEditView.as_view()),
                  path('view/<int:r_id>/<int:num>/', postr, name='postr'),
                  path('view/', view, name='view'),
                  path('', index, name='index'),

                  # url(r'^ajax/<pk>/', add_ajax),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
