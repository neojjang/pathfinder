from django.shortcuts import render
from django.views import View

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
                return render(request, 'manager-top.html', {})
            else:
                return render(request, 'student-top.html', {})
        else:
            return render(request, 'top.html', {})

class DashboardView(View):

    def get(self, request):
        return render(request, 'top.html', {})