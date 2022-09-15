from django import forms
from .models import settingmodel
category=settingmodel.objects.all()

class SettingForm(forms.Form):
    category=forms.ModelChoiceField(queryset=category,empty_label="请选择电商名称")
    hour=forms.IntegerField(max_value=24,min_value=0,label="小时")
    minute=forms.IntegerField(max_value=59,min_value=0,label="分钟")


