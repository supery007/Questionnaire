#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:supery

from django import forms

from django.forms import widgets,ValidationError

from app01 import models


class RegForm(forms.Form):
    username = forms.CharField(
        min_length=4,
        max_length=18,
        error_messages={
            'required': '请输入登录用户名',
        },
        widget=widgets.TextInput(
            attrs={'placeholder': "登录用户名，不少于4个字符", 'class': "form-control"}),

    )

    password = forms.CharField(
        min_length=6,
        max_length=18,
        error_messages={
            'required': '请输入密码',
        },
        widget=widgets.PasswordInput(
            attrs={'placeholder': "至少6位，必须含有数字", 'class': "form-control"}),
    )

    repeat_pwd = forms.CharField(
        min_length=6,
        error_messages={
            'required': '请输入确认密码',
        },
        widget=widgets.PasswordInput(attrs={'placeholder': "请输入确认密码", 'class': "form-control"}),
    )

    def clean_username(self):
        if not models.UserInfo.objects.filter(username=self.cleaned_data.get('username')):
            return self.cleaned_data.get('username')
        else:
            raise ValidationError('用户名已经存在')



    def clean_passsword(self):
        data=self.cleaned_data.get('password')
        if not data.isdigit():
            return self.cleaned_data.get('password')
        else:
            raise ValidationError('密码不能是纯数字')



    def clean_nickname(self):
        if not models.UserInfo.objects.filter(nickname=self.cleaned_data.get('nickname')):
            return self.cleaned_data.get('nickname')
        else:
            raise ValidationError('昵称已注册,请重新输入')

    # 方式二：全局钩子
    def clean(self):
        if self.cleaned_data.get('password') == self.cleaned_data.get('repeat_pwd'):
            return self.cleaned_data
        else:
            raise ValidationError('两次密码不一致')

