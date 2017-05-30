#-*- coding: utf-8 -*-
'''
Created by yoonju on 2017. 5. 30.
'''


from django import template


register = template.Library()

@register.filter
def get_score(quiz, student):
    student_score = quiz.studentscore_set.filter(student=student).order_by('-update_date')
    if len(student_score) == 0:
        return '미참가'
    return student_score[0].score


@register.filter
def get_studentscore_list(quiz, student):
    student_score = quiz.studentscore_set.filter(student=student).order_by('-update_date')
    return student_score