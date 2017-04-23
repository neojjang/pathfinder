from django.conf.urls import url
from .views import delete_question, delete_quiz
from .views import QuestionListView, QuestionDetailView, QuestionEditView, \
    ExamListView, ExamEditView, ExamDetailView

urlpatterns = [
    url(r'^exam/create/$', ExamEditView.as_view(), name='create_quiz'),
    url(r'^exam/(\d+)/$', ExamDetailView.as_view(), name='show_quiz'),
    url(r'^exam/(\d+)/edit/$', ExamEditView.as_view(), name='edit_quiz'),
    url(r'^exam/(\d+)/delete/$', delete_quiz, name='delete_quiz'),
    url(r'^exams/$', ExamListView.as_view(), name='show_quiz_list'),

    url(r'^question/create/$', QuestionEditView.as_view(), name='create_question'),
    url(r'^question/(\d+)/$', QuestionDetailView.as_view(), name='show_question'),
    url(r'^question/(\d+)/edit/$', QuestionEditView.as_view(), name='edit_question'),
    url(r'^question/(\d+)/delete/$', delete_question, name='delete_question'),
    url(r'^questions/$', QuestionListView.as_view(), name='show_question_list'),
]