
from django.conf.urls import url
from .views import take_quiz, ExamListView # ,view_list,

urlpatterns = [
    url(r'^test/(\d+)/$', take_quiz, name='start_exam'),
    # url(r'^$', view_list, name='view_list'),
    url(r'^list/$', ExamListView.as_view(), name='view_list'),
]