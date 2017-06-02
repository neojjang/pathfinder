#-*- coding: utf-8 -*-
import logging
from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse
from django.contrib.admin.views.decorators import staff_member_required
from django.http.response import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
# from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Quiz, QuestionExample, Question, Explanations
from .forms import QuizForm, QuestionForm, QuestionExampleForm, ExplanationsForm, QuizQuestionForm
from common.models import LEVEL_CHOICES, TYPE_CHOICES
from accounts.models import Student
# Create your views here.

log = logging.getLogger(__name__)

class StaffMemberRequiredMixin(object):
    @method_decorator(staff_member_required)
    def dispatch(self, request, *args, **kwargs):
        return super(StaffMemberRequiredMixin, self).dispatch(request, *args, **kwargs)


class QuestionListView(StaffMemberRequiredMixin, View):
    def get(self, request):
        page = request.GET.get('p')
        level_id = request.GET.get("level")
        question_type_id = request.GET.get("question_type")
        log.info(request.GET)

        if (not level_id or level_id == 'all') and (not question_type_id or question_type_id == 'all'):
            questions = Question.objects.all().order_by('-pk')
        else:
            query = Q();
            if level_id and level_id != 'all':
                query = Q(level=level_id)
                level_id = int(level_id)
            if question_type_id and question_type_id != 'all':
                query = query & Q(question_type=question_type_id)
                question_type_id = int(question_type_id)
            log.info(query)
            questions = Question.objects.filter(query).order_by('-pk')

        paginator = Paginator(questions, 20)
        try:
            questions = paginator.page(page)
        except PageNotAnInteger:
            questions = paginator.page(1)
        except EmptyPage:
            questions = paginator.page(paginator.num_pages)

        level = [{"id": id, "title": title} for id, title in LEVEL_CHOICES]
        question_type = [{"id": id, "title": title} for id, title in TYPE_CHOICES]

        return render(request, 'quiz/question_list.html', {
            'questions': questions,
            'level': level,
            'level_id': level_id,
            'question_type': question_type,
            'question_type_id': question_type_id
        })



class QuestionDetailView(StaffMemberRequiredMixin, View):
    def get(self, request, pk=None):
        question = get_object_or_404(Question, pk=pk)
        no_ui = request.GET.get("no_ui")
        template_file = 'quiz/question.html'
        if no_ui == 'yes':
            template_file = 'quiz/question_no_ui.html'
        return render(request, template_file, {
            'question': question,
            'no_ui': no_ui
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
                Quiz.objects.filter(questions=question).delete()
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

    def post(self, request, pk=None):
        exam = get_object_or_404(Quiz, pk=pk)
        log.debug(request.POST)
        cmd = request.POST.get("cmd")
        questions = request.POST.getlist("questions")
        students = request.POST.getlist("students")
        if cmd == 'add':
            log.debug(questions)
            if questions and len(questions) > 0:
                for id in questions:
                    exam.questions.add(Question.objects.get(pk=id))
                exam.save()
        elif cmd == 'delete':
            if questions:
                for id in questions:
                    exam.questions.remove(Question.objects.get(pk=id))
                exam.save()
        elif cmd == 'add-member':
            log.debug(students)
            if students:
                for id in students:
                    log.debug('add-member.id=%s', id)
                    exam.students.add(Student.objects.get(pk=id))
                exam.save()
        elif cmd == 'delete-member':
            if students:
                for id in students:
                    exam.students.remove(Student.objects.get(pk=id))
                exam.save()

        # my_obj.categories.add(fragmentCategory.objects.get(id=1))
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


class ExamAppendQuestionView(StaffMemberRequiredMixin, View):
    def get(self, request, pk=None):
        page = request.GET.get('p')
        level_id = request.GET.get("level")
        question_type_id = request.GET.get("question_type")
        log.info(request.GET)

        try:
            exam = Quiz.objects.get(pk=pk)
        except Quiz.DoesNotExist:
            exam = None
        if (not level_id or level_id == 'all') and (not question_type_id or question_type_id == 'all'):
            questions = Question.objects.all().order_by('-pk')
        else:
            query = Q();
            if level_id and level_id != 'all':
                query = Q(level=level_id)
                level_id = int(level_id)
            if question_type_id and question_type_id != 'all':
                query = query & Q(question_type=question_type_id)
                question_type_id = int(question_type_id)
            log.info(query)
            questions = Question.objects.filter(query).order_by('-pk')

        log.debug("level_id=[%s]" % level_id)
        paginator = Paginator(questions, 20)
        try:
            questions = paginator.page(page)
        except PageNotAnInteger:
            questions = paginator.page(1)
        else:
            questions = paginator.page(paginator.num_pages)


        level = [{"id": id, "title": title} for id, title in LEVEL_CHOICES]
        question_type = [{"id": id, "title": title} for id, title in TYPE_CHOICES]
        return render(request, 'quiz/exam_append_question.html', {
            'exam': exam,
            'questions': questions,
            'level': level,
            'question_type': question_type,
            'level_id': level_id,
            'question_type_id': question_type_id
        })
    def post(self, request, pk=None):

        pass

class ExamAddMemberView(StaffMemberRequiredMixin, View):
    def get(self, request, pk=None):
        page = request.GET.get('p')
        level_id = request.GET.get('level')
        grade_id = request.GET.get('grade')
        log.info(request.GET)

        try:
            quiz = Quiz.objects.get(pk=pk)
        except Quiz.DoesNotExist:
            quiz = None
        if (not level_id or level_id =='all') and (not grade_id or grade_id == 'all'):
            students = Student.objects.all().order_by('-pk')
        else:
            query = Q(is_activated=True)
            if level_id != 'all':
                query = Q(level=level_id)
                level_id = int(level_id)
            if grade_id != 'all':
                query = query & Q(grade=grade_id)
                grade_id = int(grade_id)
            log.info(query)
            students = Student.object.filter(query).order_by('-pk')
        paginator = Paginator(students, 20)
        try:
            students = paginator.page(page)
        except PageNotAnInteger:
            students = paginator.page(1)
        except EmptyPage:
            students = paginator.page(paginator.num_pages)
        level = [{"id": id, "title": title} for id, title in LEVEL_CHOICES]
        grade = [{"id": id, "title": title} for id, title in Student.GRADE_CHOICES]
        return render(request, 'quiz/exam_append_member.html', {
            'quiz': quiz,
            'students': students,
            'level': level,
            'grade': grade,
            'level_id': level_id,
            'grade_id': grade_id
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



@staff_member_required
def add_questions(request):
    pass