#-*- coding: utf-8 -*-
import logging
from datetime import datetime, timedelta
from django.shortcuts import render
from django.views import View
from django.utils import timezone
# from django.db import Q

from quiz.models import StudentScore
# Create your views here.

log = logging.getLogger(__name__)

def view_top(request):
    '''
    탑 화면 구성
    :param request: 
    :return: 
    '''
    return render(request, 'top.html', {})


class TopView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            # 학생/선생님에 따라 대시보드가 다름
            today = datetime.today()
            this_month = datetime(year=datetime.today().year, month=datetime.today().month, day=1)
            this_month = timezone.make_aware(this_month, timezone.get_current_timezone())
            today = datetime(year=today.year, month=today.month, day=today.day)
            today = timezone.make_aware(today, timezone.get_current_timezone())
            last_weeks = today - timedelta(days=7)
            if request.user.is_staff:
                this_month_tested_student = StudentScore.objects.filter(
                    create_date__gt=this_month
                )
                today_tested_student = StudentScore.objects.filter(
                    create_date__gt=today
                )

                latest_tested_student_10 = StudentScore.objects.filter(create_date__gte=last_weeks)
                return render(request, 'manager-top.html', {
                    'this_month_tested_students': this_month_tested_student,
                    'today_tested_students': today_tested_student,
                    'latest_tested_students': latest_tested_student_10
                })
            else:
                latest_tested_exam = request.user.student.studentscore_set.filter(
                    create_date__gte=last_weeks
                ).order_by('-create_date')
                # 참여하지 않은 테스트들 중에서 최근 등록 된 것을 보여준다.
                log.debug([score.quiz.id for score in StudentScore.objects.filter(
                    student=request.user.student
                )])
                exam_list = request.user.student.quiz_set.all().exclude(
                    id__in=[score.quiz.id for score in StudentScore.objects.filter(
                        student=request.user.student
                    )]
                ).order_by('-pk')
                # Quiz.objects.filter(students=request.user.student)

                score_list = StudentScore.get_score_list(request.user.student)

                return render(request, 'student-top.html', {
                    'tested_exam': latest_tested_exam,
                    'exam_list': exam_list,
                    'score_list': score_list,
                })
        else:
            return render(request, 'top.html', {})

class DashboardView(View):

    def get(self, request):
        return render(request, 'top.html', {})