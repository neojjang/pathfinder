from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from quiz.models import Quiz
# Create your views here.



class ExamListView(View):
    @login_required
    def get(self, request):
        return self.show_list(request)

    @login_required
    def post(self, request):
        return self.show_list(request)

    def show_list(self, request):
        exam_list = Quiz.objects.filter(students=request.user)
        return render(request, 'exam/exam_list.html', {
            'exam_list': exam_list
        })

# @login_required
# def view_list(request):
#     pass



@login_required
def take_quiz(request, quiz_no, order_no):
    pass
