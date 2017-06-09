# -*- coding:utf-8 -*-
import logging
from django.shortcuts import render
from django.views import View
from django.db.models import Q
from django.core.paginator import PageNotAnInteger, Paginator, EmptyPage
from django.shortcuts import render, reverse, redirect, get_object_or_404
# from django.contrib.admin.views.decorators import staff_member_required
# from django.utils.decorators import method_decorator

from common.models import LEVEL_CHOICES
from accounts.models import Student
from quiz.views import StaffMemberRequiredMixin
from .forms import StudentForm
# Create your views here.

log = logging.getLogger(__name__)


class ListMemberView(StaffMemberRequiredMixin, View):
    def get(self, request):
        page = request.GET.get('p')
        level_id = request.GET.get('level')
        grade_id = request.GET.get('grade')
        log.info(request.GET)
        if (not level_id or level_id == 'all') and (not grade_id or grade_id == 'all'):
            students = Student.objects.all().order_by('-pk')
        else:
            query = Q()
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
        return render(request, 'management/list_member.html', {
            'students': students,
            'level': level,
            'grade': grade,
            'level_id': level_id,
            'grade_id': grade_id
        })



class DetailMemberView(StaffMemberRequiredMixin, View):
    def get(self, request, pk=None):
        student = get_object_or_404(Student, pk=pk)

        return render(request, 'management/detail_member.html', {
            'student': student
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