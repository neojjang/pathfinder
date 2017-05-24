#-*- coding: utf-8 -*-
from django.utils.encoding import python_2_unicode_compatible
from django.db import models
from common.models import LEVEL_CHOICES
# Create your models here.


@python_2_unicode_compatible
class Question(models.Model):
    '''
    문제 관리
    '''


    level = models.IntegerField(
        verbose_name=u"문제 수준",
        choices=LEVEL_CHOICES, default=0)
    title = models.CharField(
        verbose_name=u"문제",
        max_length=100)
    text = models.CharField(
        verbose_name=u"지문",
        max_length=30000)
    limit_time = models.PositiveSmallIntegerField(
        verbose_name=u"제한시간(초)",
        default=100
    )
    correct = models.CharField(
        verbose_name=u"정답 답안",
        max_length=512
    )
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural=u"문제 은행"
        verbose_name=u"문제 은행"
    def __str__(self):
        return "{} [{}]".format(self.title, self.get_level_display())



@python_2_unicode_compatible
class QuestionExample(models.Model):
    '''
    각 문제에 들어가는 보기
    '''
    question = models.OneToOneField(Question)
    ex_sentence_1 = models.CharField(
        verbose_name=u"보기1",
        max_length=100, blank=True)
    ex_sentence_2 = models.CharField(
        verbose_name=u"보기2",
        max_length=100, blank=True)
    ex_sentence_3 = models.CharField(
        verbose_name=u"보기3",
        max_length=100, blank=True)
    ex_sentence_4 = models.CharField(
        verbose_name=u"보기4",
        max_length=100, blank=True)
    ex_sentence_5 = models.CharField(
        verbose_name=u"보기5",
        max_length=100, blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)


@python_2_unicode_compatible
class Explanations(models.Model):
    question = models.OneToOneField(Question)
    video = models.FileField(upload_to="", null=True, blank=True)
    content = models.CharField(max_length=2000, null=True, blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural=u"문제 설명 관리"
        verbose_name=u"문제 설명 관리"

    def __str__(self):
        return "설명: {}".format(self.question.title[:30])


@python_2_unicode_compatible
class Quiz(models.Model):
    '''
    퀴즈(시험) 관리
    '''
    level = models.IntegerField(
        verbose_name=u"퀴즈 수준",
        choices=LEVEL_CHOICES, default=0)
    title = models.CharField(
        verbose_name=u"퀴즈 제목",
        max_length=50)
    starting_date = models.DateTimeField(
        verbose_name=u"퀴즈 시작 날짜",
        null=True, blank=True)
    closing_date = models.DateTimeField(
        verbose_name=u"퀴즈 마감 날짜",
        null=True, blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name=u"퀴즈 관리"
        verbose_name_plural=u"퀴즈 관리"
    def __str__(self):
        return "{}[{}]".format(self.title, self.get_level_display())


@python_2_unicode_compatible
class Exam(models.Model):
    '''
    퀴즈별 할당한 문제들 매핑 관리
    '''
    quiz = models.ForeignKey(Quiz)
    question = models.ForeignKey(Question)
    order = models.IntegerField(verbose_name=u"문제 번호", default=1)
    create_date = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name_plural=u"문제지 관리"
        verbose_name=u"문제지 관리"
        ordering=['quiz', 'order']
    def __str__(self):
        return "{}-{}번-{}".format(self.quiz.id, self.order,
                              self.question.title[:20])