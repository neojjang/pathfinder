from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.



@login_required
def view_list(request):
    pass



@login_required
def take_quiz(request, quiz_no, order_no):
    pass
