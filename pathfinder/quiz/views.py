from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.views.generic import View
from .models import Quiz, QuestionExample, Question, Exam, Explanations
# Create your views here.



@staff_member_required
def create_quiz(request):
    # exam = Exam()
    # exam.question_id = 1
    # exam.quiz_id = 1
    # exam.save()
    # # or
    # Exam(quiz_id=1, question_id=1).save()
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


@staff_member_required
def get_question_list(request):
    '''
    시험지의 수준에 해당하지만 현재 선택 된 적이 없는 문제들을 검색해서 반환한다. 
    :param request: 
    :return: 
    '''
    level = request.GET.get("level")
    question_list =
    pass


# @staff_member_required
# def make_test_paper(request):
#     pass