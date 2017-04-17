from django.contrib import admin
from .models import Quiz, Question, QuestionExample, Explanations
# Register your models here.


admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(QuestionExample)
admin.site.register(Explanations)