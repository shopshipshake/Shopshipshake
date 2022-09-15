"""crawldjango URL Configuration

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
from django.contrib import admin
from django.urls import path,re_path,include
import xadmin
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from django.contrib.auth import views as v
from .settings import MEDIA_ROOT
from crawlmodel import views


xadmin.autodiscover()

urlpatterns = [
    path('xadmin/', xadmin.site.urls),
    path(r'^ueditor/',include('DjangoUeditor.urls')),
    path(r'xadmin/test_view/',views.TestView.as_view()),
    re_path('^password_reset/(?P<P>.*)/$', v.PasswordResetConfirmView.as_view())

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


#+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)