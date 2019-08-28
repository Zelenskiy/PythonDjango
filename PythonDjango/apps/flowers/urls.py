from django.urls import path, include
from django.conf.urls import url
from PythonDjango import settings
from flowers import views

from django.conf.urls.static import static

urlpatterns = [
                  url(r'^add_simple_flower/$', views.add_simple_flower, name='add_simple_flower'),

]
