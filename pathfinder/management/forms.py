#-*- coding: utf-8 -*-
'''
Created by yoonju on 2017. 6. 9.
'''
from django import forms

from common.models import LEVEL_CHOICES
from accounts.models import Student, Teacher, Lecture, LectureSchedule



class StudentForm(forms.ModelForm):
    class Meta:
        model=Student
        fields = ('school_name', 'grade', 'level', 'is_activated')
        widgets = {
            'school_name': forms.TextInput(attrs={'class': 'form-control'}),
            'grade': forms.Select(attrs={'class': 'form-control'}),
            'level': forms.Select(attrs={'class': 'form-control'}),
            # 'is_activated': forms.CheckboxInput(attrs={'class': 'form-control'})
        }

class TeacherForm(forms.ModelForm):
    class Meta:
        model=Teacher
        fields = ('is_admin', 'is_activated')
        # widgets = {
        #     'is_activated': forms.CheckboxInput(attrs={'class': 'form-control'}),
        #     'is_admin': forms.CheckboxInput(attrs={'class': 'form-control'})
        # }


class LectureForm(forms.ModelForm):
    class Meta:
        model = Lecture
        fields = ('title', 'grade', 'teacher', 'students')
        widgets = {
            'teacher': forms.Select(attrs={'class': 'form-control'}),
            'students': forms.CheckboxSelectMultiple(attrs={'class': 'form-control'})
        }


class LectureScheduleForm(forms.ModelForm):
    class Meta:
        model = LectureSchedule
        fields = ('weekday', 'from_time', 'to_time')