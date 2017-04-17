from django.conf.urls import url
from .views import dashboard, view_detail

urlpatterns = [
    url(r'^(\d+)/$', view_detail, name='view_detail'),
    url(r'^$', dashboard, name='dashboard'),
]