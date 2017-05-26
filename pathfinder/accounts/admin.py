from django.contrib import admin
from .models import Student
from quiz.models import StudentScore, StudentAnswer
# Register your models here.

admin.site.register(Student)
admin.site.register(StudentScore)
admin.site.register(StudentAnswer)