from django.contrib import admin
from .models import Quiz, Question, QuestionExample, Explanations
# Register your models here.

class AdminQuestionExample(admin.StackedInline):
    model = QuestionExample


class AdminQuestion(admin.ModelAdmin):
    model = Question

    inlines = [
        AdminQuestionExample
    ]

admin.site.register(Quiz)
admin.site.register(Question, AdminQuestion)
admin.site.register(QuestionExample)
admin.site.register(Explanations)