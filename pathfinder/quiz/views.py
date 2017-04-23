#-*- coding: utf-8 -*-
import logging
from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse
from django.contrib.admin.views.decorators import staff_member_required
from django.http.response import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
# from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Quiz, QuestionExample, Question, Exam, Explanations
from .forms import QuizForm, QuestionForm, QuestionExampleForm, ExplanationsForm
# Create your views here.

log = logging.getLogger(__name__)

class StaffMemberRequiredMixin(object):
    @method_decorator(staff_member_required)
    def dispatch(self, request, *args, **kwargs):
        return super(StaffMemberRequiredMixin, self).dispatch(request, *args, **kwargs)


class QuestionListView(StaffMemberRequiredMixin, View):
    def get(self, request):
        page = request.GET.get('p')

        questions = Question.objects.all().order_by('-pk')
        paginator = Paginator(questions, 20)
        try:
            questions = paginator.page(page)
        except PageNotAnInteger:
            questions = paginator.page(1)
        except EmptyPage:
            questions = paginator.page(paginator.num_pages)

        return render(request, 'quiz/question_list.html', {
            'questions': questions
        })



class QuestionDetailView(StaffMemberRequiredMixin, View):
    def get(self, request, pk=None):
        question = get_object_or_404(Question, pk=pk)

        return render(request, 'quiz/question.html', {
            'question': question
        })


class QuestionEditView(StaffMemberRequiredMixin, View):
    def get(self, request, pk=None):
        try:
            question = Question.objects.get(pk=pk)
            question_form = QuestionForm(instance=question)
        except Question.DoesNotExist:
            question_form = QuestionForm()
            question = None

        try:
            question_example = QuestionExample.objects.get(
                question=question
            )
            question_example_form = QuestionExampleForm(
                instance=question_example
            )
        except QuestionExample.DoesNotExist:
            question_example_form = QuestionExampleForm()

        try:
            explanation = Explanations.objects.get(
                question=question
            )
            explanation_form = ExplanationsForm(
                instance=explanation
            )
        except Explanations.DoesNotExist:
            explanation_form = ExplanationsForm()

        return render(request, 'quiz/question_edit.html', {
            'pk': pk,
            'question': question,
            'question_form': question_form,
            'question_example_form': question_example_form,
            'explanation_form': explanation_form
        })

    def post(self, request, pk=None):
        try:
            question = Question.objects.get(pk=pk)
        except Question.DoesNotExist:
            question = None

        question_form = QuestionForm(request.POST, instance=question)
        question_example_form = QuestionExampleForm(request.POST, instance=question)
        # if request.FILE:
        explanation_form = ExplanationsForm(request.POST, request.FILES, instance=question)
        # else:
        #     explanation_form = ExplanationsForm(request.POST)

        if question_form.is_valid() \
                and question_example_form.is_valid() \
                and explanation_form.is_valid():
            question = question_form.save()
            question_example = question_example_form.save(commit=False)
            question_example.question = question
            question_example.save()
            explanation = explanation_form.save(commit=False)
            explanation.question = question
            explanation.save()

            return redirect(reverse('quiz:show_question', args=[question.pk]))

        return render(request, 'quiz/question_edit.html', {
            'question_form': question_form,
            'question_example_form': question_example_form,
            'explanation_form': explanation_form
        })


@staff_member_required
def create_quiz(request):
    pass



@staff_member_required
def delete_question(request, pk=None):
    if pk:
        try:
            question = Question.objects.get(pk=pk)
            try:
                question_example = QuestionExample.objects.get(question=question)
                question_example.delete()
            except QuestionExample.DoesNotExist:
                pass
            try:
                explanation = Explanations.objects.get(question=question)
                explanation.delete()
            except Explanations.DoesNotExist:
                pass
            try:
                Exam.objects.filter(question=question).delete()
            except Exception as e:
                log.error(e)
                pass
            question.delete()
        except Question.DoesNotExist:
            pass

    return redirect(reverse('quiz:show_question_list'))



class ExamListView(StaffMemberRequiredMixin, View):
    def get(self, request):
        page = request.GET.get('p')
        quizes = Quiz.objects.all().order_by('-pk')
        paginator = Paginator(quizes, 20)
        try:
            quizes = paginator.page(page)
        except PageNotAnInteger:
            quizes = paginator.page(1)
        except EmptyPage:
            quizes = paginator.page(paginator.num_pages)

        return render(request, 'quiz/exam_list.html', {
            'quizes': quizes
        })


class ExamDetailView(StaffMemberRequiredMixin, View):
    def get(self, request, pk=None):
        exam = get_object_or_404(Quiz, pk=pk)
        return render(request, 'quiz/exam.html', {
            'exam': exam
        })



class ExamEditView(StaffMemberRequiredMixin, View):

    def get_exam(self, pk):
        try:
            exam = Quiz.objects.get(pk=pk)
        except Quiz.DoesNotExist:
            exam = None
        return exam

    def get(self, request, pk=None):
        exam = self.get_exam(pk)
        form = QuizForm(instance=exam)

        return render(request, 'quiz/exam_edit.html', {
            'form': form,
            'quiz': exam
        })

    def post(self, request, pk=None):
        exam = self.get_exam(pk)
        form = QuizForm(request.POST, instance=exam)
        if form.is_valid():
            form.save()
            return redirect(reverse('quiz:show_quiz_list'))
        return render(request, 'quiz/exam_edit.html', {
            'form': form,
            'quiz': exam
        })


@staff_member_required
def delete_quiz(request, pk=None):
    if pk:
        try:
            quiz = Quiz.objects.get(pk=pk)
            try:
                Exam.objects.filter(quiz=quiz).delete()
            except Exception as e:
                log.error(e)
                pass
            quiz.delete()
        except Quiz.DoesNotExist:
            pass

    return redirect(reverse('quiz:show_quiz_list'))



@staff_member_required
def get_question_list(request):
    '''
    시험지의 수준에 해당하지만 현재 선택 된 적이 없는 문제들을 검색해서 반환한다. 
    :param request: 
    :return: 
    '''
    quiz_id = request.GET.get("q") # 문제지 번호
    level = request.GET.get("level")
    quiz = Quiz.objects.get(pk=quiz_id)
    exams = quiz.exam_set.all()
    current_questions = exams.values_list("question_id", flat=True)
    question_list = Question.objects.filter(level=level).exclude(id__in=current_questions)
    values = question_list.values('id', 'title', 'text')
    return JsonResponse(values)



# @staff_member_required
# def make_test_paper(request):
#     pass