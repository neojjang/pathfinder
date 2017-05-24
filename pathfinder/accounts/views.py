#-*- coding: utf-8 -*-
import logging
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, StudentRedistrationForm
from .models import Student, StudentExam, StudentAnswer, StudentScore
# Create your views here.

log = logging.getLogger(__name__)


def regist_member(request):
    '''
    학생 정보를 등록 
    :param request: 
    :param pk: 
    :return: 
    '''
    if request.method == 'POST':
        form = StudentRedistrationForm(request.POST)
        if form.is_valid():
            new_student = form.save(commit=False)
            new_student.set_password(form.cleaned_data['password'])
            new_student.save()

            student = Student(user=new_student)
            student.save()

            return render(request, 'member/registration_done.html', {'new_student':new_student})
    else:
        form = StudentRedistrationForm()
    return render(request, 'member/registration.html', {
        'form': form
    })


@staff_member_required
def modify_member(request, pk):
    '''
    학생 정보를 수정
    :param request: 
    :param pk: 
    :return: 
    '''
    pass


@staff_member_required
def list_member(request):
    '''
    User(is_staff=False)인 학생 목록 페이지
    :param request: 
    :return: 
    '''
    pass

@staff_member_required
def view_member(request):
    '''
    User(is_staff=False)인 학생 목록 페이지
    :param request: 
    :return: 
    '''
    pass

@staff_member_required
def edit_member(request):
    '''
    User(is_staff=False)인 학생 목록 페이지
    :param request: 
    :return: 
    '''
    pass


@login_required
def view_profile(request):
    '''
    학생이 로그인 후 자기 정보를 보는 페이지
    :param request: 
    :return: 
    '''
    try:
        student = Student.objects.get(user=request.user)
    except Student.DoesNotExist:
        student = Student(user=request.user)
        student.save()

    quiz_results = StudentScore.objects.filter(exam__student=student)

    return render(request, 'member/mypage.html', {
        'student': student,
        'quiz_results': quiz_results
    })



# def login_view(request):
#     log.debug("login_view")
#     if request.method == "POST":
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             cleaned_data = form.cleaned_data
#             user = authenticate(username=cleaned_data['username'],
#                                 password=cleaned_data['password'])
#             if user is not None:
#                 if user.is_active:
#                     login(request, user)
#                     return # authenticated successfully
#                 else:
#                     return # disable user
#
#             form.add_error('username', '아이디 또는 비밀번호를 확인해주세요.')
#         log.debug(form.errors)
#
#     else:
#         form = LoginForm()
#
#     log.error(form.errors)
#     return render(request, '', {
#         'form': form
#     })

# @login_required
# def logout_view(request):
#     logout(request)
#     return HttpResponseRedirect(redirect_to='/')

