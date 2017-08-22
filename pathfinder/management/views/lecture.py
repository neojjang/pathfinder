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
from accounts.models import Student, Teacher
from management.models import Lecture, LectureSchedule
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
            lectures = Lecture.objects.all().order_by('-pk')
            log.debug(100)
        else:
            lectures = request.user.teacher.lecture_set.all().order_by('-pk')
            log.debug(10000)
        log.debug(lectures)
        paginator = Paginator(lectures, 10)
        log.debug(paginator)
        try:
            lectures = paginator.page(page)
            log.debug(1)
        except PageNotAnInteger:
            lectures = paginator.page(1)
            log.debug(2)
        except EmptyPage:
            lectures = paginator.page(paginator.num_pages)
            log.debug(3)

        log.debug(lectures)
        lecture_form = LectureForm(
            initial={
                'teacher': request.user.teacher if not request.user.teacher.is_admin else None
            }
        )
        ScheduleFormSet = formset_factory(LectureScheduleForm, can_delete=True)
        schedule_form = ScheduleFormSet() # LectureScheduleForm()

        students = Student.objects.filter(is_activated=True)

        return render(request, 'management/list_lecture.html', {
            'lecture_list': lectures,
            'page': page,
            'form': lecture_form,
            'schedule_formset': schedule_form,
            'students': students
        })
    def post(self, request):
        lecture_form = LectureForm(request.POST)
        ScheduleFormSet = formset_factory(LectureScheduleForm, can_delete=True)
        schedule_form = ScheduleFormSet(request.POST)
        if lecture_form.is_valid() & schedule_form.is_valid():
            lecture = lecture_form.save()
            log.debug(lecture)
            for form in schedule_form.forms:
                schedule = form.save(commit=False)
                schedule.lecture = lecture
                schedule.save()
            return JsonResponse({"status":"OK"})
        else:
            log.debug(lecture_form.errors.items())
            log.debug(schedule_form.errors)
            error = {key: value for key, value in lecture_form.errors.items()}
            error.update({key: value for key, value in schedule_form.errors})
            error.update({"status": "ERROR"})
            return JsonResponse(error)


class EditLectureView(StaffMemberRequiredMixin, View):
    def get(self, request, pk=None, cmd='edit'):
        return render(request, 'management/list_lecture.html', {})

    def post(self, request, pk=None, cmd='edit'):
        return render(request, 'management/list_lecture.html', {})