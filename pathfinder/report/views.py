from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View

from quiz.models import Quiz, StudentAnswer, StudentScore
# Create your views here.



class DetailView(LoginRequiredMixin, View):
    def get(self, request, exam_id):
        exam = get_object_or_404(Quiz, pk=exam_id)

        student_score = StudentScore.objects.filter(
            quiz=exam,
            student=request.user.student
        ).order_by('-pk')

        return render(request, 'report/detail_view.html', {
            'exam': exam,
            'score_list': student_score
        })



@login_required
def dashboard(request):
    pass