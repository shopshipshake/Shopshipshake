from django.contrib.auth.models import AbstractBaseUser
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from .forms import SettingForm
from xadmin.views import CommAdminView
import time, hashlib


class TestView(CommAdminView):
    def get(self, request):
        form = SettingForm()
        return render(request, 'form.html', context={'form': form})

    def post(self, request):
        form = SettingForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            hour = form.cleaned_data.get('hour')
            minute = form.cleaned_data.get('minute')
            return HttpResponse("suceess")  # 最后指定自定义的template模板，并返回context
        else:
            print("表单报错",form.errors)
            return HttpResponse("false")
