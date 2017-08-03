#-*- coding: utf-8 -*-
'''
Created by yoonju on 2017. 8. 3.
'''
import logging
from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from django.db.models import Q
from django.db.models.aggregates import Max, Count
from django.core.paginator import PageNotAnInteger, Paginator, EmptyPage
from django.shortcuts import render, reverse, redirect, get_object_or_404
# from django.contrib.admin.views.decorators import staff_member_required
# from django.utils.decorators import method_decorator

from common.models import LEVEL_CHOICES
from accounts.models import Student, Teacher
from quiz.models import StudentScore
from quiz.views import StaffMemberRequiredMixin
from management.forms import StudentForm
from accounts.forms import StudentRedistrationForm
# Create your views here.

log = logging.getLogger(__name__)


class LessonView(View):
    def get(self, request, pk=None):
        return render(request, 'management/detail_lesson.html', {})



class ListLessonView(View):
    def get(self, request):
        return render(request, 'management/list_lesson.html', {})


class EditLessonView(View):
    def get(self, request):
        return render(request, 'management/list_lesson.html', {})