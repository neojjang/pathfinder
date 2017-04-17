#-*- coding: utf-8 -*-

from django.conf.urls import url
from accounts.views import regist_member, list_member, modify_member, view_profile
from django.contrib.auth.views import login, logout, password_change, password_change_done

urlpatterns = [
    url(r'^login/$', login, name='login'),
    url(r'^logout/$', logout, name='logout'),

    url(r'^register/$', regist_member, name='regist'),
    url(r'^list/$', list_member, name='list'),
    url(r'^modify/(\d+)/$', modify_member, name='modify'),

    url(r'^profile/$', view_profile, name='view_profile'),
]