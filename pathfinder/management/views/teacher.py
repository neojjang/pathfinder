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
from management.forms import TeacherForm
from accounts.forms import StudentRedistrationForm
# Create your views here.

log = logging.getLogger(__name__)


class ListTeacherView(StaffMemberRequiredMixin, View):
    def get(self, request):
        page = request.GET.get('p')
        teachers = Teacher.objects.all()

        paginator = Paginator(teachers, 20)
        try:
            teachers = paginator.page(page)
        except PageNotAnInteger:
            teachers = paginator.page(1)
        except EmptyPage:
            teachers = paginator.page(paginator.num_pages)

        form = StudentRedistrationForm()
        teacher_form = TeacherForm()
        return render(request, 'management/list_teacher.html', {
            'teachers': teachers,
            'page': page,
            'form': form,
            'teacher_form': teacher_form
        })
    def post(self, request):
        '''
        선생님을 등록 처리
        '''
        user_form = StudentRedistrationForm(request.POST)
        teacher_form = TeacherForm(request.POST)
        if user_form.is_valid() and teacher_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.is_staff = True
            new_user.save()

            student = teacher_form.save(commit=False)
            student.user = new_user
            student.save()
            return  JsonResponse({"status": "OK"}) # redirect(reverse("quiz:list_member"))
        else:
            log.debug(user_form.errors.items())
            log.debug(teacher_form.errors.items())
            error = {key:value for key, value in user_form.errors.items()}
            error.update({key:value for key, value in teacher_form.errors.items()})
            error.update({"status": "ERROR"})
            return JsonResponse(error)


class DetailTeacherView(StaffMemberRequiredMixin, View):
    def get(self, request, pk=None):
        teacher = get_object_or_404(Teacher, pk=pk)
        lesson_list = teacher.get_my_lesson()
        page = request.GET.get('p')
        paginator = Paginator(lesson_list, 20)
        try:
            lesson_list = paginator.page(page)
        except PageNotAnInteger:
            lesson_list = paginator.page(1)
        except EmptyPage:
            lesson_list = paginator.page(paginator.num_pages)
        return render(request, 'management/detail_teacher.html', {
            'teacher': teacher,
            'lesson_list' : lesson_list
        })


class EditTeacherView(StaffMemberRequiredMixin, View):
    def get(self, request, pk=None, cmd='edit'):
        teacher = get_object_or_404(Teacher, pk=pk)
        return render(request, 'management/edit_teacher.html', {
            'teacher': teacher
        })

    def post(self, request, pk=None, cmd='edit'):
        teacher = get_object_or_404(Teacher, pk=pk)
        if cmd == 'edit':
            return render(request, 'management/edit_teacher.html', {
                'teacher': teacher
            })
        else:
            return redirect(reverse('quiz:list_teacher'))