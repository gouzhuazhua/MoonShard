# -*- coding: utf-8 -*-
# @Time    : 2018/12/17 15:46
# @Author  : Invoker
# @FileName: forms.py
# @Software: PyCharm

from django.core.exceptions import ValidationError
from django import forms
from ckeditor.fields import RichTextFormField


class NewTopicForm(forms.Form):
    title = forms.CharField(label='标题',
                            max_length=100,
                            widget=forms.TextInput(attrs={'id': 'title', 'placeholder': '请输入主题标题'}),
                            error_messages={'required': '标题不能为空'})
    subject = RichTextFormField(label='内容')

    def clean_title(self):
        title = self.cleaned_data.get('title')
        return title
