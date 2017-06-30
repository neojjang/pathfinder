#-*- coding: utf-8 -*-
import logging
from django.utils.encoding import python_2_unicode_compatible
from django.db import models
from django.utils import timezone

from common.models import LEVEL_CHOICES, TYPE_CHOICES
from accounts.models import Student
# Create your models here.

log = logging.getLogger(__name__)

@python_2_unicode_compatible
class Question(models.Model):
    '''
    문제 관리
    '''
    ANSWER_TYPE_CHOICES=((0, "객관식"), (1,"주관식-단답형"), (2,"다중선택"), (3, "주관식-서술형"),)
    level = models.IntegerField(
        verbose_name=u"문제 수준",
        choices=LEVEL_CHOICES, default=0)
    question_type = models.IntegerField(
        verbose_name=u"문제 유형",
        choices=TYPE_CHOICES,
        default=0
    )
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
    answer_type = models.IntegerField(
        verbose_name=u"답변 방식",
        choices=ANSWER_TYPE_CHOICES,
        default=0
    )
    correct = models.CharField(
        verbose_name=u"정답 답안",
        max_length=2000
    )
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural=u"문제 은행"
        verbose_name=u"문제 은행"
    def __str__(self):
        return "{} [{}]".format(self.title, self.get_level_display())
    def get_used_count(self):
        return self.quiz_set.all().count()



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
    content = models.CharField(max_length=5000, null=True, blank=True)
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
    테스트(시험) 관리
    '''
    level = models.IntegerField(
        verbose_name=u"테스트 수준",
        choices=LEVEL_CHOICES, default=0)
    title = models.CharField(
        verbose_name=u"테스트 제목",
        max_length=50)
    starting_date = models.DateTimeField(
        verbose_name=u"테스트 시작 날짜",
        null=True, blank=True)
    closing_date = models.DateTimeField(
        verbose_name=u"테스트 마감 날짜",
        null=True, blank=True)
    questions = models.ManyToManyField(Question, verbose_name=u"문제")
    students = models.ManyToManyField(Student, verbose_name=u"학생")
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name=u"퀴즈 관리"
        verbose_name_plural=u"퀴즈 관리"
        ordering=['-pk']
    def __str__(self):
        return "{}[{}]".format(self.title, self.get_level_display())

    def get_latest_score(self, student):
        student_score = self.studentscore_set.filter(student=student).order_by('-update_date')
        if len(student_score) == 0: return 'X'
        return student_score[0].score
    def is_timeover(self):
        return self.closing_date < timezone.now()
    def get_percent_ratio(self):
        question_count = self.questions.all().count()
        studentscore_list = self.studentscore_set.all()
        ratio = 0.0
        for student in studentscore_list:
            ratio = ratio + (student.score / question_count)

        if len(studentscore_list) > 0:
            return ratio / len(studentscore_list)
        else:
            return 0.0



@python_2_unicode_compatible
class StudentScore(models.Model):
    '''
    같은 시험을 몇번이고 볼 수 있다는 가정으로 각 시험의 점수를 별도로 저장 
    '''
    quiz = models.ForeignKey(Quiz)
    student = models.ForeignKey(Student)
    ekey = models.CharField(verbose_name=u"테스트키",
                            max_length=14,
                            default="",
                            null=False,
                            blank=False)
    score = models.PositiveSmallIntegerField(verbose_name=u"맞은 수", default=0)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name=u"성적"
        verbose_name_plural=u"성적"
        ordering=['-pk',]

    def __str__(self):
        return "{}-{}시험-{}점".format(self.student.get_name(),
                                    self.quiz.title,
                                    self.score)
    def get_answers(self):
        return StudentAnswer.objects.filter(ekey=self.ekey).order_by('pk')
    def get_result_by_type(self):
        '''
        유형별 결과
        :return:
        '''
        answer_list = StudentAnswer.objects.filter(ekey=self.ekey)
        result = {}
        for answer in answer_list:
            qt = answer.question.get_question_type_display()
            if not result.get(qt): result[qt] = [0,0]
            result[qt][0] = result[qt][0] + 1
            if answer.is_correct:
                result[qt][1] = result[qt][1] + 1
        log.debug(result)
        return result


@python_2_unicode_compatible
class StudentAnswer(models.Model):
    '''
    각 시험의 문제별 학생이 입력한 답을 저장, 관리
    '''
    quiz = models.ForeignKey(Quiz)
    student = models.ForeignKey(Student)
    question = models.ForeignKey(Question)
    ekey = models.CharField(verbose_name=u"테스트키",
                            max_length=14,
                            default="",
                            null=False,
                            blank=False)
    answer = models.CharField(verbose_name=u"학생 답",
                              max_length=512,
                              blank=True, default='')
    elapsed_time = models.PositiveIntegerField(verbose_name=u"걸린 시간",
                                       default=0)
    is_correct = models.BooleanField(verbose_name=u"정답?",
                                     default=False)
    show_explain = models.BooleanField(verbose_name=u"해설 봤음?",
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
    def get_show_explain_display(self):
        return "O" if self.show_explain else "X"
    def get_is_correct_display(self):
        return "O" if self.is_correct else  "X"