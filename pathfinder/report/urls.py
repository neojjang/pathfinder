from django.conf.urls import url
from .views import dashboard, DetailView

urlpatterns = [
    url(r'^(\d+)/$', DetailView.as_view(), name='view_detail'),
    url(r'^$', dashboard, name='dashboard'),
]