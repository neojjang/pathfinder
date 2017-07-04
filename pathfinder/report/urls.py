from django.conf.urls import url
from .views import DashboardView, DetailView, StudentScoreView

urlpatterns = [
    url(r'^(\d+)/detail/$', DetailView.as_view(), name='view_detail'),
    url(r'^(\d+)/$', StudentScoreView.as_view(), name='view_score'),
    url(r'^$', DashboardView.as_view(), name='dashboard'),

]