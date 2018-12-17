from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django import forms
from .models import User

import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')


class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email')


class UpdateForm(forms.Form):
    SEX_CHOICE = (
        ('0', '未确认'),
        ('1', '男'),
        ('2', '女'),
    )
    sex = forms.ChoiceField(label='性别',
                            choices=SEX_CHOICE,
                            widget=forms.RadioSelect(attrs={'id': 'sex', 'placeholder': '请选择性别'}),
                            error_messages={'required': '性别不能为空'})
    age = forms.IntegerField(label='年龄',
                             max_value=99,
                             widget=forms.NumberInput(attrs={'id': 'age', 'placeholder': '请输入年龄'}),
                             error_messages={'required': '年龄不能为空'})

    def clean_sex(self):
        sex = self.cleaned_data.get('sex')
        return sex

    def clean_age(self):
        age = self.cleaned_data.get('age')
        return age
