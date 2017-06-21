
import logging
from datetime import datetime

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import PageNotAnInteger, Paginator, EmptyPage
from django.views.generic import View
from django.http import JsonResponse
from quiz.models import Quiz
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

@login_required
def save_answer(request, exam_id=None):
    '''
    시험 각 문제의 답을 저장한다.
    StudentAnswer
    '''
    data = {}
    return JsonResponse(data)



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

    def post(self, request):
        log.debug(request.META)
        log.debug(request.POST)
        return render(request, 'exam/take_exam.html', {

        })


class SaveAnswerView(LoginRequiredMixin, View):
    def post(self, request, pk):
        log.debug(request.META)
        log.debug(request.POST)
        log.debug("exam=%s", pk)
        pass