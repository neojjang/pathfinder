# -*- coding:utf-8 -*-
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
from accounts.models import Student
from quiz.models import StudentScore
from quiz.views import StaffMemberRequiredMixin
from .forms import StudentForm
from accounts.forms import StudentRedistrationForm
# Create your views here.

log = logging.getLogger(__name__)


class ListMemberView(StaffMemberRequiredMixin, View):
    def get(self, request):
        page = request.GET.get('p')
        level_id = request.GET.get('level')
        grade_id = request.GET.get('grade')
        log.info(request.GET)
        if (not level_id or level_id == 'all') and (not grade_id or grade_id == 'all'):
            students = Student.objects.filter(user__is_staff=False).order_by('-pk')
        else:
            query = Q(user__is_staff=False)
            if level_id != 'all':
                query = query & Q(level=level_id)
                level_id = int(level_id)
            if grade_id != 'all':
                query = query & Q(grade=grade_id)
                grade_id = int(grade_id)
            students = Student.objects.filter(query).order_by('-pk')

        paginator = Paginator(students, 20)

        try:
            students = paginator.page(page)
        except PageNotAnInteger:
            students = paginator.page(1)
        except EmptyPage:
            students = paginator.page(paginator.num_pages)

        level = [{"id": id, "title": title} for id, title in LEVEL_CHOICES]
        grade = [{"id": id, "title": title} for id, title in Student.GRADE_CHOICES]

        form = StudentRedistrationForm()
        student_form = StudentForm()
        return render(request, 'management/list_member.html', {
            'students': students,
            'level': level,
            'grade': grade,
            'level_id': level_id,
            'grade_id': grade_id,
            'form': form,
            'student_form': student_form
        })
    def post(self, request):
        user_form = StudentRedistrationForm(request.POST)
        student_form = StudentForm(request.POST)
        if user_form.is_valid() and student_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()

            student = student_form.save(commit=False)
            student.user = new_user
            student.save()
            return  JsonResponse({"status": "OK"}) # redirect(reverse("quiz:list_member"))
        else:
            log.debug(user_form.errors.items())
            log.debug(student_form.errors.items())
            error = {key:value for key, value in user_form.errors.items()}
            error.update({key:value for key, value in student_form.errors.items()})
            error.update({"status": "ERROR"})
            return JsonResponse(error)



class DetailMemberView(StaffMemberRequiredMixin, View):
    def get(self, request, pk=None):
        page = request.GET.get('p')
        student = get_object_or_404(Student, pk=pk)
        score_list = StudentScore.get_score_list(student)

        quiz_list = student.quiz_set.all()
        paginator = Paginator(quiz_list, 20)
        try:
            quiz_list = paginator.page(page)
        except PageNotAnInteger:
            quiz_list = paginator.page(1)
        except EmptyPage:
            quiz_list = paginator.page(paginator.num_pages)

        log.debug(student.id)

        # score_list = StudentScore.objects.annotate(Max('score'))
        # log.debug(score_list.query)

        return render(request, 'management/detail_member.html', {
            'student': student,
            'quiz_list': quiz_list,
            'score_list': score_list
        })



class EditMemberView(StaffMemberRequiredMixin, View):
    def get(self, request, pk=None):
        student = get_object_or_404(Student, pk=pk)
        form = StudentForm(instance=student)
        return render(request, 'management/edit_member.html', {
            'student': student,
            'form': form
        })

    def post(self, request, pk=None):
        message = None
        student = get_object_or_404(Student, pk=pk)

        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            message = u"수정 되었습니다."
        else:
            log.error(form.errors)
        return render(request, 'management/edit_member.html', {
            'student': student,
            'form': form,
            'message': message
        })