
from django.conf.urls import url
from .views import TakeExamView, ExamListView, SaveAnswerView # ,view_list,

urlpatterns = [
    url(r'^test/(\d+)/$', TakeExamView.as_view(), name='take_exam'),
    # url(r'^$', view_list, name='view_list'),
    url(r'^list/$', ExamListView.as_view(), name='view_list'),

    url(r'save-answer/(\d+)/$', SaveAnswerView.as_view(), name='save_answer'),

]