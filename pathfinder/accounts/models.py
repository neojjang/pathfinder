#-*- coding: utf-8 -*-

from django.utils.encoding import python_2_unicode_compatible
from django.db import models
from django.conf import settings
from common.models import LEVEL_CHOICES
from quiz.models import Quiz, Question
# Create your models here.

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


@python_2_unicode_compatible
class StudentResults(models.Model):
    student =models.ForeignKey(Student)
    quiz = models.ForeignKey(Quiz)
    score = models.PositiveSmallIntegerField(verbose_name=u"점수", default=0)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name=u"성적"
        verbose_name_plural=u"성적"

    def __str__(self):
        return "{}-{}시험-{}점".format(self.student.get_name(),
                                    self.quiz.title,
                                    self.score)


@python_2_unicode_compatible
class StudentAnswer(models.Model):
    student = models.ForeignKey(Student)
    quiz = models.ForeignKey(Quiz, default=None)
    question = models.ForeignKey(Question)
    answer = models.CharField(verbose_name=u"학생 답",
                              max_length=512,
                              blank=True, default='')
    is_correct = models.BooleanField(verbose_name=u"정답?",
                                     default=False)
    create_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural=u"학생 답안지"
        verbose_name=u"학생 답안지"

    def __str__(self):
        return "{} {}번:{}:{}".format(
            self.student.get_name(),
            self.question.id,
            self.answer,
            self.is_correct
        )