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
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include
# from bboard.views import index
from PythonDjango import settings
from PythonDjango.views import main
from bboard.views import index
from plan.views import MyRegisterFormView

urlpatterns = [

                  path('admin/', admin.site.urls),
                  path('bboard/', include('bboard.urls')),
                  path('plan/', include('plan.urls')),

                  # path('', include('plan.urls')),
                  # url(r'^flowers/', include('flowers.urls')),
                  path('registration/register/', MyRegisterFormView.as_view(), name="register"),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Add Django site authentication urls (for login, logout, password management)
urlpatterns += [
    url(r'^accounts/', include('django.contrib.auth.urls')),

]
