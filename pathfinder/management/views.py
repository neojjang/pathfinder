# -*- coding:utf-8 -*-
from django.shortcuts import render
from django.views import View
from django.db.models import Q
from django.core.paginator import PageNotAnInteger, Paginator, EmptyPage
from django.shortcuts import render, reverse, redirect
# from django.contrib.admin.views.decorators import staff_member_required
# from django.utils.decorators import method_decorator

from quiz.views import StaffMemberRequiredMixin
# Create your views here.


class ListMemberView(StaffMemberRequiredMixin, View):
    def get(self, request):
        return render(request, '', {})



class DetailMemberView(StaffMemberRequiredMixin, View):
    def get(self, request, pk=None):
        return render(request, '', {})



class EditMemberView(StaffMemberRequiredMixin, View):
    def get(self, request, pk=None):
        return render(request, '', {})

    def post(self, request, pk=None):
        return render(request, '', {})