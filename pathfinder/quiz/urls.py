from django.conf.urls import url
from .views import show_quiz, show_quiz_list, show_question, show_question_list, \
    create_quiz, create_question, edit_quiz, edit_question

urlpatterns = [
    url(r'^test-paper/create/$', create_quiz, name='create_quiz'),
    url(r'^test-paper/(\d+)/$', show_quiz, name='show_quiz'),
    url(r'^test-paper/(\d+)/edit/$', edit_quiz, name='edit_quiz'),
    url(r'^test-paper/$', show_quiz_list, name='show_quiz_list'),

    url(r'^question/create/$', create_question, name='create_question'),
    url(r'^question/(\d+)/$', show_question, name='show_question'),
    url(r'^question/(\d+)/edit/$', edit_question, name='edit_question'),
    url(r'^question/$', show_question_list, name='show_question_list'),

    # url(r'^test-paper/$', make_test_paper, name='make_test_paper'),
]