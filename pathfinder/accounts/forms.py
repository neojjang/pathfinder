#-*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from common.models import LEVEL_CHOICES
from accounts.models import Student

class StudentRedistrationForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['username', 'first_name', 'last_name', 'email']

    first_name = forms.CharField(label='first_name', max_length=20, required=True)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('비밀번호가 일치 하지 않습니다.')
        return cd['password2']


class StudentForm(forms.ModelForm):
    school_name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={}),
        label=u"학교 이름"
    )
    grade = forms.ChoiceField(
        choices=Student.GRADE_CHOICES,
        widget=forms.Select(attrs={}),
        label=u"학생의 학년"
    )
    level = forms.ChoiceField(
        choices=LEVEL_CHOICES,
        widget=forms.Select,
        label=u"학생의 현재 수준"
    )
    is_activated = forms.BooleanField(
        widget=forms.CheckboxInput,
        label=u"등원중"
    )
    class Meta:
        model = Student
        fields = ('school_name', 'grade', 'level', 'is_activated')



class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)