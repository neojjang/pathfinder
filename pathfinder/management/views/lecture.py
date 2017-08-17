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
from django.forms.formsets import formset_factory
# from django.contrib.admin.views.decorators import staff_member_required
# from django.utils.decorators import method_decorator

from common.models import LEVEL_CHOICES
from accounts.models import Student, Teacher, Lecture, LectureSchedule
from quiz.views import StaffMemberRequiredMixin
from management.forms import StudentForm, LectureForm, LectureScheduleForm
# Create your views here.

log = logging.getLogger(__name__)


class DetailLectureView(StaffMemberRequiredMixin, View):
    def get(self, request, pk=None):
        lecture = get_object_or_404(Lecture, pk=pk)
        student_list = lecture.students.all()
        return render(request, 'management/detail_lecture.html', {
            'lecture': lecture,
            'student_list': student_list
        })



class ListLectureView(StaffMemberRequiredMixin, View):
    def get(self, request):
        page = request.GET.get('p')
        if request.user.teacher.is_admin:
            lecture_list = Lecture.objects.all()
        else:
            lecture_list = request.user.teacher.lecture_set.all()

        paginator = Paginator(lecture_list, 20)
        try:
            lecture_list = paginator.page(page)
        except PageNotAnInteger:
            lecture_list = paginator.page(1)
        except EmptyPage:
            lecture_list = paginator.page(paginator.num_pages)

        lecture_form = LectureForm(
            initial={
                'teacher': request.user.teacher if not request.user.teacher.is_admin else None
            }
        )
        ScheduleFormSet = formset_factory(LectureScheduleForm, can_delete=True)
        schedule_form = ScheduleFormSet() # LectureScheduleForm()

        students = Student.objects.all()

        return render(request, 'management/list_lecture.html', {
            'lecture_list': lecture_list,
            'page': page,
            'form': lecture_form,
            'schedule_formset': schedule_form,
            'students': students
        })


class EditLectureView(StaffMemberRequiredMixin, View):
    def get(self, request, pk=None, cmd='edit'):
        return render(request, 'management/list_lecture.html', {})

    def post(self, request, pk=None, cmd='edit'):
        return render(request, 'management/list_lecture.html', {})