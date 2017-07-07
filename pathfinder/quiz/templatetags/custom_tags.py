#-*- coding: utf-8 -*-
'''
Created by yoonju on 2017. 5. 30.
'''

import logging
from django import template


log = logging.getLogger(__name__)


register = template.Library()

@register.filter
def get_score(quiz, student):
    student_score = quiz.studentscore_set.filter(student=student).order_by('-score')
    if len(student_score) == 0:
        return None
    return student_score[0]

# @register.filter
# def get_score(quiz, student):
#     student_score = quiz.studentscore_set.filter(student=student).order_by('-score')
#     if len(student_score) == 0:
#         return None
#     return student_score[0].score


@register.filter
def get_studentscore_list(quiz, student):
    student_score = quiz.studentscore_set.filter(student=student).order_by('-update_date')
    return student_score


@register.filter
def percentratio_of_question_exam(question, quiz):
    student_count = quiz.students.all().count()
    studentscore_count = quiz.studentscore_set.all().count()
    # log.debug(student_count)
    # log.debug(studentscore_count)
    student_count = student_count if student_count >= studentscore_count else studentscore_count
    question_count = quiz.studentanswer_set.filter(question=question).count()
    # 퀴즈의 모든 문제는 최소 학생수 만큼의 답지를 갖고 있어야 한다.
    question_count = question_count if question_count >= student_count else student_count
    log.debug(question_count)
    correct_count = quiz.studentanswer_set.filter(question=question,
                                                  is_correct=True).count()
    if question_count > 0:
        return correct_count*100 / question_count
    else:
        return 0