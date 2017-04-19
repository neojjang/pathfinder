
from django.conf.urls import url
from .views import take_quiz, ExamListView # ,view_list,

urlpatterns = [
    url(r'^(\d+)/(\d+)/$', take_quiz, name='take_quiz'),
    # url(r'^$', view_list, name='view_list'),
    url(r'^$', ExamListView.as_view, name='view_list'),
]