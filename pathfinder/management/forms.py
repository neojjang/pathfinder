#-*- coding: utf-8 -*-
'''
Created by yoonju on 2017. 6. 9.
'''
from django import forms

from common.models import LEVEL_CHOICES
from accounts.models import Student



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
