#-*- coding: utf-8 -*-
'''
Created by yoonju on 2017. 5. 24.
'''
from django.conf.urls import url
from quiz.views import delete_question, delete_quiz
from quiz.views import QuestionListView, QuestionDetailView, QuestionEditView, \
    ExamListView, ExamEditView, ExamDetailView, ExamAppendQuestionView, \
    ExamAddMemberView
from .views.member import ListMemberView, DetailMemberView, EditMemberView
from .views.teacher import ListTeacherView, DetailTeacherView, EditTeacherView
from .views.lecture import DetailLectureView, ListLectureView, EditLectureView

urlpatterns = [
    url(r'^exam/create/$', ExamEditView.as_view(), name='create_quiz'),
    url(r'^exam/(\d+)/$', ExamDetailView.as_view(), name='show_quiz'),
    url(r'^exam/(\d+)/edit/$', ExamEditView.as_view(), name='edit_quiz'),
    url(r'^exam/(\d+)/delete/$', delete_quiz, name='delete_quiz'),
    url(r'^exam/(\d+)/questions/$', ExamAppendQuestionView.as_view(), name='append_question'),
    url(r'^exam/(\d+)/add-member/$', ExamAddMemberView.as_view(), name='add_member'),
    url(r'^exams/$', ExamListView.as_view(), name='show_quiz_list'),

    url(r'^question/create/$', QuestionEditView.as_view(), name='create_question'),
    url(r'^question/(\d+)/$', QuestionDetailView.as_view(), name='show_question'),
    url(r'^question/(\d+)/edit/$', QuestionEditView.as_view(), name='edit_question'),
    url(r'^question/(\d+)/delete/$', delete_question, name='delete_question'),
    url(r'^questions/$', QuestionListView.as_view(), name='show_question_list'),

    url(r'^student/list/$', ListMemberView.as_view(), name='list_member'),
    url(r'^student/(\d+)/$', DetailMemberView.as_view(), name='show_member'),
    url(r'^student/(\d+)/(edit|delete)/$', EditMemberView.as_view(), name='edit_member'),
    # url(r'^student/(\d+)/delete/$', EditMemberView.as_view(), name='delete_member'),

    url(r'^teacher/list/$', ListTeacherView.as_view(), name='list_teacher'),
    url(r'^teacher/(\d+)/$', DetailTeacherView.as_view(), name='show_teacher'),
    url(r'^teacher/(\d+)/(edit|delete)/$', EditTeacherView.as_view(), name='edit_teacher'),
    # url(r'^teacher/(\d+)/delete/$', EditTeacherView.as_view(), name='delete_teacher')

    url(r'^lecture/list/$', ListLectureView.as_view(), name='list_lecture'),
    url(r'^lecture/(\d+)/$', DetailLectureView.as_view(), name='show_lecture'),
    url(r'^lecture/(\d+)/(edit|delete)/$', EditLectureView.as_view(), name='create_lecture'),

]