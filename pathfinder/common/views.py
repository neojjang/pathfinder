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
        return render(request, 'top.html', {})

class DashboardView(View):

    def get(self, request):
        return render(request, 'top.html', {})