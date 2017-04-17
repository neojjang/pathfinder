from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.views.generic import View
# Create your views here.



@staff_member_required
def create_quiz(request):
    pass



@staff_member_required
def edit_quiz(request):
    pass


@staff_member_required
def show_quiz_list(request):
    pass


@staff_member_required
def show_quiz(request):
    pass


@staff_member_required
def create_question(request):
    pass


@staff_member_required
def edit_question(request):
    pass


@staff_member_required
def show_question_list(request):
    pass


@staff_member_required
def show_question(request):
    pass


# @staff_member_required
# def make_test_paper(request):
#     pass