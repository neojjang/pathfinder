#-*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, StudentRedistrationForm
from .models import Student, StudentExam, StudentAnswer
# Create your views here.

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


@login_required
def view_profile(request):
    '''
    학생이 로그인 후 자기 정보를 보는 페이지
    :param request: 
    :return: 
    '''
    student = Student.objects.get(user=request.user)
    quiz_results = StudentResults.objects.filter(student=student)

    return render(request, 'member/mypage.html', {
        'student': student,
        'quiz_results': quiz_results
    })



def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            user = authenticate(username=cleaned_data['username'],
                                password=cleaned_data['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return # authenticated successfully
                else:
                    return # disable user
    else:
        form = LoginForm()
    return render(request, '', {
        'form': form
    })

@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(redirect_to='/')

