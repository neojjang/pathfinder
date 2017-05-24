#-*- coding: utf-8 -*-
'''
Created by yoonju on 2017. 5. 24.
'''
from django.conf.urls import url
from quiz.views import delete_question, delete_quiz
from quiz.views import QuestionListView, QuestionDetailView, QuestionEditView, \
    ExamListView, ExamEditView, ExamDetailView, ExamAppendQuestion
from accounts.views import list_member, view_member, edit_member

urlpatterns = [
    url(r'^exam/create/$', ExamEditView.as_view(), name='create_quiz'),
    url(r'^exam/(\d+)/$', ExamDetailView.as_view(), name='show_quiz'),
    url(r'^exam/(\d+)/edit/$', ExamEditView.as_view(), name='edit_quiz'),
    url(r'^exam/(\d+)/delete/$', delete_quiz, name='delete_quiz'),
    url(r'^exam/(\d+)/questions/$', ExamAppendQuestion.as_view(), name='append_question'),
    url(r'^exams/$', ExamListView.as_view(), name='show_quiz_list'),

    url(r'^question/create/$', QuestionEditView.as_view(), name='create_question'),
    url(r'^question/(\d+)/$', QuestionDetailView.as_view(), name='show_question'),
    url(r'^question/(\d+)/edit/$', QuestionEditView.as_view(), name='edit_question'),
    url(r'^question/(\d+)/delete/$', delete_question, name='delete_question'),
    url(r'^questions/$', QuestionListView.as_view(), name='show_question_list'),

    url(r'^student/list/$', list_member, name='list_member'),
    url(r'^student/(\d+)/$', view_member, name='show_member'),
    url(r'^student/(\d+)/edit/$', edit_member, name='edit_member'),
]