from django.shortcuts import render
from django.views import View

from quiz.models import StudentScore
# Create your views here.


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
            if request.user.is_staff:
                latest_tested_student = StudentScore.objects.all()[:10]
                return render(request, 'manager-top.html', {
                    'tested_students': latest_tested_student
                })
            else:
                latest_tested_exam = request.user.student.studentscore_set.all()
                # 참여하지 않은 테스트들 중에서 최근 등록 된 것을 보여준다.
                exam_list = request.user.student.quiz_set.all().order_by('-pk')[:5]
                # Quiz.objects.filter(students=request.user.student)

                return render(request, 'student-top.html', {
                    'tested_exam': latest_tested_exam,
                    'exam_list': exam_list
                })
        else:
            return render(request, 'top.html', {})

class DashboardView(View):

    def get(self, request):
        return render(request, 'top.html', {})