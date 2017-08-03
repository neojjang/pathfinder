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
    is_activated = models.BooleanField(default=False, verbose_name=u"등원여부")
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

@python_2_unicode_compatible
class Teacher(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    is_admin = models.BooleanField(default=False)
    is_activated = models.BooleanField(default=False, verbose_name=u"활성화")
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name_plural=u"선생님"
        verbose_name=u"선생님"
    def __str__(self):
        return "{}{} 선생님".format(self.user.last_name,
                         self.user.first_name)

    def get_questions(self):
        return self.question_set.all()
    def get_quiz(self):
        return self.quiz_set.all()
    def get_my_grades(self):
        grade_choices = dict(Student.GRADE_CHOICES)
        grade = []
        for item in self.lesson_set.all().values('grade').distinct():
            grade.append(grade_choices[item.get('grade')])
        return grade
    def get_my_lesson(self):
        return self.lesson_set.all()
    def get_my_students(self):
        return Student.objects.filter(lesson__teacher=self)
    def get_my_students_count(self):
        # print("get_my_students_count=", self.get_my_students().count())
        return self.get_my_students().count()


@python_2_unicode_compatible
class Lesson(models.Model):
    title = models.CharField(default="", verbose_name=u"수업이름",
                            max_length=30)
    grade = models.IntegerField(choices=Student.GRADE_CHOICES, default=0,
                                verbose_name=u"학년")
    teacher = models.ForeignKey(Teacher)
    students = models.ManyToManyField(Student)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name=u"수업"
        verbose_name_plural=u"수업"
    def __str__(self):
        return self.title
    def get_students_count(self):
        return self.students.count()
    def get_schedules(self):
        return self.lessonschedule_set.all()


@python_2_unicode_compatible
class LessonSchedule(models.Model):
    WEEKDAY_CHOICES = ((1, '일'), (2, '월'), (3, '화'), (4, '수'),
                       (5, '목'), (6, '금'), (7, '토'))
    lesson = models.ForeignKey(Lesson)
    weekday = models.IntegerField(choices=WEEKDAY_CHOICES, verbose_name=u"수업요일")
    from_time = models.TimeField(verbose_name=u"~부터", auto_now=True)
    to_time = models.TimeField(verbose_name=u"~까지", auto_now=True)
    class Meta:
        verbose_name_plural=u"수업시간표"
        verbose_name=u"수업시간표"
    def __str__(self):
        return "{} 시간표".format(self.lesson.title)