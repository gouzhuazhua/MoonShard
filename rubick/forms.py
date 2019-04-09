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
                            widget=forms.TextInput(attrs={'id': 'title',
                                                          'placeholder': '请输入主题标题',
                                                          'class': 'mdl-textfield__input'}),
                            error_messages={'required': '标题不能为空'})
    subject = RichTextFormField(label='内容',
                                max_length=4000,
                                widget=forms.Textarea(attrs={'id': 'subject',
                                                             'placeholder': '请在此输入内容'}),
                                required=False)

    def clean_title(self):
        title = self.cleaned_data.get('title')
        return title

    def clean_subject(self):
        subject = self.cleaned_data.get('subject')
        return subject



class PostForm(forms.Form):
    topic_id = forms.CharField(label='',
                               widget=forms.TextInput(attrs={'id': 'topic_id', 'type': 'hidden'}),
                               required=True)
    post = RichTextFormField(label='',
                             max_length=4000,
                             widget=forms.Textarea(attrs={'id': 'post', 'placeholder': '请在此输入内容'}),
                             required=True)

    def clean_post(self):
        post = self.cleaned_data.get('post')
        return post

    def clean_topic_id(self):
        topic_id = self.cleaned_data.get('topic_id')
        return topic_id


class ReplyForm(forms.Form):
    post_id = forms.CharField(label='',
                              widget=forms.TextInput(attrs={'id': 'post_id', 'type': ''}),
                              required=True)
    reply = RichTextFormField(label='',
                              max_length=4000,
                              widget=forms.Textarea(attrs={'id': 'reply', 'placeholder': '请在此输入内容'}),
                              required=True)

    def clean_reply(self):
        reply = self.cleaned_data.get('reply')
        return reply

    def clean_post_id(self):
        post_id = self.cleaned_data.get('post_id')
        return post_id
