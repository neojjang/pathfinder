from django.contrib import admin
from .models import Student, StudentAnswer, StudentResults
# Register your models here.

admin.site.register(Student)
admin.site.register(StudentAnswer)
admin.site.register(StudentResults)