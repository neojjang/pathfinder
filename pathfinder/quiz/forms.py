#-*- coding: utf-8 -*-
from django import forms
from common.models import LEVEL_CHOICES
from .models import QuestionType, Quiz, Question, Answer, Explanations

class QuizForm(forms.Form):
    '''
    
    '''
    pass


class TotalQuestionForm(forms.Form):
    '''
    form에 문제(Question)+답예문(Answer)+설명(Explanations) 정의
    뷰에서 각각에 맞게 객체를 생성할 때 사용한다.
    '''
    # Question --------------
    question_type=forms.ModelChoiceField(
        queryset=QuestionType.objects.all(),
        widget=forms.Select(attrs={}),
        label=u"문제 유형을 선택해 주세요."
    )
    level = forms.ChoiceField(
        choices=LEVEL_CHOICES,
        widget=forms.Select(attrs={}),
        label=u"문제 수준을 선택해 주세요."
    )
    title = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={}),
        label=u"문제를 입력해 주세요."
    )
    text = forms.CharField(
        max_length=4000,
        widget=forms.Textarea(attrs={}),
        label=u"문제 지문을 규칙에 맞게 입력해 주세요."
    )
    # Answer -----------------
    objective_answer = forms.IntegerField(
        min_value=1,
        widget=forms.TextInput(attrs={}),
        label=u"객관식 정답 번호를 입력해 주세요."
    )
    subjective_answer = forms.CharField(
        max_length=512,
        widget=forms.TextInput(attrs={}),
        label=u"주관식 정답을 입력해 주세요"
    )
    ex_sentence_1 = forms.CharField(max_length=100, blank=True,
                                    label=u"규칙에 맞게 객관식 문항을 입력하세요.")
    ex_sentence_2 = forms.CharField(max_length=100, blank=True,
                                    label=u"규칙에 맞게 객관식 문항을 입력하세요.")
    ex_sentence_3 = forms.CharField(max_length=100, blank=True,
                                    label=u"규칙에 맞게 객관식 문항을 입력하세요.")
    ex_sentence_4 = forms.CharField(max_length=100, blank=True,
                                    label=u"규칙에 맞게 객관식 문항을 입력하세요.")
    ex_sentence_5 = forms.CharField(max_length=100, blank=True,
                                    label=u"규칙에 맞게 객관식 문항을 입력하세요.")
    # Explanations ---------------
    video = forms.FileField(upload_to="media/", null=True, blank=True)
    content = forms.CharField(max_length=2000, null=True, blank=True)

# class QuestionForm(forms.Form):
#     '''
#
#     '''
#     pass
# class AnswerForm(forms.Form):
#     '''
#
#     '''
#     pass
#
#
# class Explanations(forms.Form):
#     '''
#
#     '''
#     pass