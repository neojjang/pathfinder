from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.


@login_required
def view_detail(request):
    pass



@login_required
def dashboard(request):
    pass