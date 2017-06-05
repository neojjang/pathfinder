from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import PageNotAnInteger, Paginator, EmptyPage
from django.views.generic import View
from quiz.models import Quiz
# Create your views here.



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


# @login_required
# def view_list(request):
#     pass



class TakeExamView(LoginRequiredMixin, View):
    def get(self, request, pk):
        exam_list = request.user.student.quiz_set.filter(pk=pk)

        exam = exam_list[0] if len(exam_list) > 0 else None
        return render(request, 'exam/take_exam.html', {
            'exam': exam
        })

    def post(self, request):
        return render(request, 'exam/take_exam.html', {

        })