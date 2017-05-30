#-*- coding: utf-8 -*-

from django.utils.encoding import python_2_unicode_compatible
from django.db import models
from django.conf import settings
from common.models import LEVEL_CHOICES
# Create your models here.
# LEVEL_CHOICES = (
#     (1, "중1초급"), (2, "중1중급"), (3, "중1상급"),
#     (4, "중2초급"), (5, "중2중급"), (6, "중2상급"),
#     (7, "중3초급"), (8, "중3중급"), (9, "중3상급"),
#     (10, "고1초급"), (12, "고1중급"), (13, "고1상급"),
#     (14, "고2초급"), (15, "고2중급"), (16, "고2상급"),
#     (17, "고3초급"), (18, "고3중급"), (19, "고3상급"),
#     (20, "수능"), (0, "모름")
# )

@python_2_unicode_compatible
class Student(models.Model):
    GRADE_CHOICES = (
        (1, "중1학년"), (2, "중2학년"), (3, "중3학년"),
        (4, "고1학년"), (5, "고2학년"), (6, "고3학년"),
        (7, "졸업"), (0, "모름")
    )
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    school_name = models.CharField(verbose_name=u"학교",
                                   max_length=20,
                                   blank=True,
                                   default='')
    grade = models.IntegerField(verbose_name=u"학년",
                                choices=GRADE_CHOICES, default=0)
    level = models.IntegerField(verbose_name=u"학생 레벨",
                                choices=LEVEL_CHOICES, default=0)
    is_activated = models.BooleanField(default=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name=u"학생 정보"
        verbose_name_plural=u"학생 정보"

    def __str__(self):
        return "{} {} {} - ".format(self.user.last_name,
                                    self.user.first_name,
                                    self.get_grade_display(),
                                    self.get_level_display())
    def get_name(self):
        return "{} {}".format(self.user.last_name, self.user.first_name)

    def get_latest_quiz(self):
        quiz = self.studentscore_set.all().order_by('-pk')[:1]
        return quiz

    def get_latest_score(self, quiz):
        student_score = self.studentscore_set.filter(quiz=quiz).order_by('-update_date')
        if len(student_score) == 0:
            return 'X'
        else:
            return student_score[0].score

# @python_2_unicode_compatible
# class StudentExam(models.Model):
#     '''
#     학생에 할당 된 시험을 관리
#     '''
#     student = models.ForeignKey(Student)
#     quiz = models.ForeignKey(Quiz)
#     create_date = models.DateTimeField(auto_now_add=True)
#     update_date = models.DateTimeField(auto_now=True)
#
#     class Meta:
#         verbose_name_plural=u"시험 관리"
#         verbose_name=u"시험 관리"
#
#     def __str__(self):
#         return "{}-{}시험".format(self.student.get_name(), self.quiz.title)
#
