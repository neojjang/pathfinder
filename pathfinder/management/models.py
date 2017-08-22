#-*- coding: utf-8 -*-

from django.utils.encoding import python_2_unicode_compatible
from django.db import models
from django.conf import settings
from common.models import LEVEL_CHOICES

from accounts.models import Student, Teacher


@python_2_unicode_compatible
class Lecture(models.Model):
    teacher = models.ForeignKey(Teacher)
    title = models.CharField(default="", verbose_name=u"수업이름",
                            max_length=30)
    grade = models.IntegerField(choices=Student.GRADE_CHOICES, default=0,
                                verbose_name=u"학년")
    students = models.ManyToManyField(Student)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name=u"수업"
        verbose_name_plural=u"수업"
    def __str__(self):
        return "{0} [{1}{2} 선생님]".format(self.title, self.teacher.user.first_name,self.teacher.user.last_name)
    def get_students_count(self):
        return self.students.count()
    def get_schedules(self):
        return self.lectureschedule_set.all()


@python_2_unicode_compatible
class LectureSchedule(models.Model):
    WEEKDAY_CHOICES = ((0, '일'), (1, '월'), (2, '화'), (3, '수'),
                       (4, '목'), (5, '금'), (6, '토'))
    lecture = models.ForeignKey(Lecture)
    weekday = models.IntegerField(choices=WEEKDAY_CHOICES, default=0, verbose_name=u"수업요일")
    from_time = models.TimeField(verbose_name=u"~부터", default=None)
    to_time = models.TimeField(verbose_name=u"~까지", default=None)
    class Meta:
        verbose_name_plural=u"수업시간표"
        verbose_name=u"수업시간표"
    def __str__(self):
        return "{} 시간표".format(self.lecture.title)