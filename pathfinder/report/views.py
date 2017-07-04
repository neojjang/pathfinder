from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.db.models import Q
from django.core.paginator import PageNotAnInteger, Paginator, EmptyPage

from quiz.models import Quiz, StudentAnswer, StudentScore
from quiz.views import StaffMemberRequiredMixin
# Create your views here.



class StudentScoreView(LoginRequiredMixin, View):
    def get(self, request, exam_id):
        exam = get_object_or_404(Quiz, pk=exam_id)

        student_score = StudentScore.objects.filter(
            quiz=exam,
            student=request.user.student
        ).order_by('-pk')

        return render(request, 'report/score_view.html', {
            'exam': exam,
            'score_list': student_score
        })


class DetailView(LoginRequiredMixin, View):
    def get(self, request, score_id):
        query = Q(pk=score_id)
        if not request.user.is_staff:
            query = query + Q(student=request.user.student)
            template_file = 'report/detail_view.html'
        else:
            template_file = 'report/admin_detail_view.html'

        score = StudentScore.objects.get(query)

        return render(request, template_file, {
            'score': score,
            'exam': score.quiz,

        })


class DashboardView(StaffMemberRequiredMixin, View):
    def get(self, request):
        page = request.GET.get('p')

        tested_students = StudentScore.objects.all()
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


