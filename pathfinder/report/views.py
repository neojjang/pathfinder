#-*- coding: utf-8 -*-
import logging
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.db.models import Q, Max
from django.core.paginator import PageNotAnInteger, Paginator, EmptyPage

from accounts.models import Student
from quiz.models import Quiz, StudentAnswer, StudentScore
from quiz.views import StaffMemberRequiredMixin
# Create your views here.

log = logging.getLogger(__name__)

class StudentScoreView(LoginRequiredMixin, View):
    def get(self, request, exam_id):
        exam = get_object_or_404(Quiz, pk=exam_id)

        student_score = StudentScore.objects.filter(
            quiz=exam,
            student=request.user.student
        ).order_by('-pk')
        log.debug(student_score)
        exam_percent_ratio = exam.get_percent_ratio(request.user.student)
        return render(request, 'report/score_view.html', {
            'exam': exam,
            'score_list': student_score,
            'exam_percent_ratio': exam_percent_ratio
        })


class DetailView(LoginRequiredMixin, View):
    def get(self, request, score_id):
        query = Q(pk=score_id)
        if not request.user.is_staff:
            query = query & Q(student=request.user.student)
            template_file = 'report/detail_view.html'
        else:
            template_file = 'report/admin_detail_view.html'
        log.debug(query)
        score = StudentScore.objects.get(query)

        question_count = score.quiz.questions.all().count()
        ranking_list = []
        for rank in StudentScore.objects.filter(quiz=score.quiz).values(
                'quiz','student'
        ).annotate(Max('score')).order_by('-score__max')[:10]:  #.filter(quiz=score.quiz)
            rank['student'] = Student.objects.get(pk=rank['student'])
            rank['score__max'] = (rank['score__max'] * 100 ) / question_count
            ranking_list.append(rank)

        log.debug(ranking_list)
        log.debug(ranking_list[0].get('student'))
        return render(request, template_file, {
            'score': score,
            'exam': score.quiz,
            'ranking_list': ranking_list,
        })


class DashboardView(StaffMemberRequiredMixin, View):
    def get(self, request):
        page = request.GET.get('p')

        tested_students = StudentScore.objects.all().order_by('-create_date')
        paginator = Paginator(tested_students, 20)
        try:
            tested_students = paginator.page(page)
        except PageNotAnInteger:
            tested_students = paginator.page(1)
        except EmptyPage:
            tested_students = paginator.page(paginator.num_pages)

        return render(request, 'report/dashboard.html', {
            'students': tested_students,
        })


