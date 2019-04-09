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


class UpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('sex', 'age', 'introduce', 'addr', 'avatar')
    # username = forms.CharField(label='用户名',
    #                            max_length=99,
    #                            widget=forms.TextInput(attrs={'id': 'username',
    #                                                          'placeholder': '请输入主题标题',
    #                                                          'class': 'mdl-textfield__input',
    #                                                          'readonly': 'readonly'}),
    #                            )
    # SEX_CHOICE = (
    #     ('0', '未确认'),
    #     ('1', '男'),
    #     ('2', '女'),
    # )
    # sex = forms.CharField(label='性别',
    #                       widget=forms.TextInput(attrs={'id': 'sex'}),
    #                       error_messages={'required': '性别不能为空'})
    # age = forms.CharField(label='年龄',
    #                       max_length=2,
    #                       widget=forms.TextInput(attrs={'id': 'age',
    #                                                     'class': 'mdl-textfield__input',
    #                                                     'pattern': '-?[0-9]*(\.[0-9]+)?',
    #                                                     'placeholder': '请输入年龄'}),
    #                       error_messages={'required': '年龄不能为空'})
    # introduce = forms.CharField(label='个人简介',
    #                               widget=forms.Textarea(attrs={'id': 'introduce',
    #                                                            'rows': 3,
    #                                                            'class': 'mdl-textfield__input'}),)
    # addr = forms.CharField(label='公寓',
    #                        max_length=99,
    #                        widget=forms.TextInput(attrs={'id': 'addr',
    #                                                      'class': 'mdl-textfield__input'}),
    #                        )
    # # avatar = forms.FileInput()
    #
    # def clean_username(self):
    #     username = self.cleaned_data.get('username')
    #     return username
    #
    # def clean_sex(self):
    #     sex = self.cleaned_data.get('sex')
    #     return sex
    #
    # def clean_age(self):
    #     age = self.cleaned_data.get('age')
    #     return age
    #
    # def clean_introduce(self):
    #     introduce = self.cleaned_data.get('introduce')
    #     return introduce
    #
    # def clean_addr(self):
    #     addr = self.cleaned_data.get('addr')
    #     return addr
    #
    # # def clean_avatar(self):
    # #     avatar = self.cleaned_data.get('avatar')
    # #     return avatar
