
import logging
from datetime import datetime

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import PageNotAnInteger, Paginator, EmptyPage
from django.views.generic import View
from django.http import JsonResponse
from quiz.models import Quiz, Question, StudentAnswer, StudentScore
# Create your views here.


log = logging.getLogger(__name__)


class ExamListView(LoginRequiredMixin, View):
    def get(self, request):
        page = request.GET.get('p')
        exam_list = request.user.student.quiz_set.all().order_by('-pk')
            # Quiz.objects.filter(students=request.user.student)

        paginator = Paginator(exam_list, 20)
        try:
            exam_list = paginator.page(page)
        except PageNotAnInteger:
            exam_list = paginator.page(1)
        except EmptyPage:
            exam_list = paginator.page(paginator.num_pages)

        return render(request, 'exam/exam_list.html', {
            'exam_list': exam_list,
            'student': request.user.student
        })



class TakeExamView(LoginRequiredMixin, View):
    def get(self, request, pk):
        exam_key = datetime.today().strftime("%Y%m%d%H%M%S")    # datetime.strptime(str(datetime.today()), "YmdHMS")
        # 학생에게 배정된 시험만 풀 수 있다.
        exam_list = request.user.student.quiz_set.filter(pk=pk)

        exam = exam_list[0] if len(exam_list) > 0 else None

        return render(request, 'exam/take_exam.html', {
            'exam': exam,
            'exam_key': exam_key,
            'total_questions': exam.questions.all().count() if exam else 0
        })

    def post(self, request, pk):
        log.debug(request.META)
        log.debug(request.POST)

        exam_key = request.POST.get("exam-key")
        quiz = get_object_or_404(Quiz, pk=pk)
        student_answer_list = StudentAnswer.objects.filter(
            quiz=quiz,
            ekey=exam_key,
            student=request.user.student
        )
        score = 0
        for answer in student_answer_list:
            if answer.is_correct:
                score = score + 1
        log.debug("score=%s", score)
        student_score, created = StudentScore.objects.update_or_create(
            quiz=quiz,
            student=request.user.student,
            ekey=exam_key,
            defaults={
                'quiz': quiz,
                'student': request.user.student,
                'ekey': exam_key,
                'score': score
            }
        )
        log.debug("student_score=%s", student_score)
        return render(request, 'exam/ok_test.html', {
            'quiz': quiz
        })


class SaveAnswerView(LoginRequiredMixin, View):
    def post(self, request, pk):
        log.debug(request.META)
        log.debug(request.POST)
        log.debug("exam=%s", pk)
        log.debug(request.POST.keys())

        exam_key = request.POST.get("exam-key")
        current_no = int(request.POST.get("current-no"))
        qid_list = request.POST.getlist("qid")
        show_explain_list = request.POST.getlist("show-explain")
        elapsed_time_list = request.POST.getlist("elapsed-time")
        log.debug("exam_key=%s", exam_key)
        log.debug("current_no=%s", current_no)
        log.debug("qid_list=%s", qid_list)
        log.debug("show_explain_list=%s", (show_explain_list))
        log.debug("elapsed_time_list=%s", elapsed_time_list)

        qid = qid_list[current_no-1]
        log.debug("qid=%s", qid)

        quiz = get_object_or_404(Quiz, pk=pk)
        question = get_object_or_404(Question, pk=qid)
        log.debug(quiz)
        log.debug(question)

        user_answer = request.POST.get("answer-{}".format(current_no))

        log.debug("question.correct=%s", question.correct)
        log.debug("user-answer=%s", user_answer)
        student_answer, created = StudentAnswer.objects.update_or_create(
            quiz=quiz,
            student=request.user.student,
            question=question,
            ekey=exam_key,
            defaults={
                'quiz': quiz,
                'student': request.user.student,
                'question': question,
                'ekey': exam_key,
                'answer': user_answer,
                'elapsed_time': elapsed_time_list[current_no-1],
                'show_explain': show_explain_list[current_no-1],
                'is_correct': (question.correct == user_answer.strip())
            }
        )
        log.debug("student_answer=%s", student_answer)
        log.debug("created=%s", created)

        return JsonResponse({
            'current_no': current_no,
            'user_answer': user_answer,
            'created': created
        })