#-*- coding: utf-8 -*-
from django import forms
from common.models import LEVEL_CHOICES
from .models import Quiz, Question, Explanations, QuestionExample



class QuestionForm(forms.ModelForm):
    '''
    form에 문제(Question)+답예문(Answer)+설명(Explanations) 정의
    뷰에서 각각에 맞게 객체를 생성할 때 사용한다.
    '''
    # Question --------------
    level = forms.ChoiceField(
        choices=LEVEL_CHOICES,
        widget=forms.Select(attrs={}),
        label=u"문제 수준을 선택해 주세요."
    )
    title = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={}),
        required=True,
        label=u"문제를 입력해 주세요."
    )
    text = forms.CharField(
        max_length=4000,
        widget=forms.Textarea(attrs={'rows':'4'}),
        required=True,
        label=u"문제 지문을 규칙에 맞게 입력해 주세요."
    )
    limit_time = forms.IntegerField(
        min_value=60,
        widget=forms.TextInput(attrs={}),
        required=True,
        label=u"제한 시간을 초단위로 입력해 주세요."
    )
    correct = forms.CharField(
        max_length=128,
        widget=forms.TextInput(attrs={}),
        required=True,
        label=u"정답을 적어 주세요."
    )

    class Meta:
        model=Question
        fields=[
            'level', 'title', 'text', 'limit_time', 'correct'
        ]



class QuestionExampleForm(forms.ModelForm):
    ex_sentence_1 = forms.CharField(max_length=100,
                                    required=False,
                                    widget=forms.TextInput(attrs={}),
                                    label=u"규칙에 맞게 객관식 보기를 입력하세요.")
    ex_sentence_2 = forms.CharField(max_length=100,
                                    required=False,
                                    widget=forms.TextInput(attrs={}),
                                    label=u"규칙에 맞게 객관식 보기를 입력하세요.")
    ex_sentence_3 = forms.CharField(max_length=100,
                                    required=False,
                                    widget=forms.TextInput(attrs={}),
                                    label=u"규칙에 맞게 객관식 보기를 입력하세요.")
    ex_sentence_4 = forms.CharField(max_length=100,
                                    required=False,
                                    widget=forms.TextInput(attrs={}),
                                    label=u"규칙에 맞게 객관식 보기를 입력하세요.")
    ex_sentence_5 = forms.CharField(max_length=100,
                                    required=False,
                                    widget=forms.TextInput(attrs={}),
                                    label=u"규칙에 맞게 객관식 보기 입력하세요.")
    class Meta:
        model=QuestionExample
        fields = [
            'ex_sentence_1', 'ex_sentence_2', 'ex_sentence_3',
            'ex_sentence_4', 'ex_sentence_5'
        ]


class ExplanationsForm(forms.ModelForm):
    # Explanations ---------------
    video = forms.FileField(
        label=u"동영상 강의가 있다면 선택해 주세요.",
        required=False
    )
    content = forms.CharField(
        max_length=2000,
        required=False,
        widget=forms.Textarea(attrs={'rows':'4'}),
        label=u"문제 해설을 적어 주세요."
    )
    class Meta:
        model=Explanations
        fields=[
            'video', 'content'
        ]



class QuizForm(forms.ModelForm):
    '''
    
    '''
    level = forms.ChoiceField(
        choices=LEVEL_CHOICES,
        widget=forms.Select(attrs={}),
        label=u"시험 수준을 선택해 주세요."
    )
    title = forms.CharField(
        label=u"시험의 제목을 적어주세요.",
        widget=forms.TextInput(attrs={}),
        max_length=50
    )
    starting_date = forms.DateTimeField(
        label=u"시험 시작 날짜를 선택해 주세요.",
        required=False
    )
    closing_date = forms.DateTimeField(
        label=u"시험 마감 날짜를 선택해 주세요.",
        required=False
    )
    class Meta:
        model=Quiz
        fields=[
            'level', 'title', 'starting_date', 'closing_date'
        ]

