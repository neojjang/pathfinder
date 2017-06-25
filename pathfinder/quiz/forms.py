#-*- coding: utf-8 -*-
from django import forms
from common.models import LEVEL_CHOICES, TYPE_CHOICES
from .models import Quiz, Question, Explanations, QuestionExample



class QuestionForm(forms.ModelForm):
    '''
    form에 문제(Question)+답예문(Answer)+설명(Explanations) 정의
    뷰에서 각각에 맞게 객체를 생성할 때 사용한다.
    '''
    # Question --------------
    level = forms.ChoiceField(
        choices=LEVEL_CHOICES,
        widget=forms.Select(attrs={'class':'form-control'}),
        label=u"문제 수준을 선택해 주세요."
    )
    question_type = forms.ChoiceField(
        choices=TYPE_CHOICES,
        widget=forms.Select(attrs={'class':'form-control'}),
        label=u"문제 유형을 선택해 주세요."
    )
    title = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class':'form-control'}),
        required=True,
        label=u"문제를 입력해 주세요."
    )
    text = forms.CharField(
        max_length=4000,
        widget=forms.Textarea(attrs={'rows':'20', 'class':'form-control'}),
        required=True,
        label=u"문제 지문을 입력해 주세요."
    )
    limit_time = forms.IntegerField(
        min_value=60,
        max_value=120,
        widget=forms.NumberInput(attrs={'class':'form-control'}),
        required=True,
        label=u"제한 시간을 초단위로 입력해 주세요."
    )
    answer_type = forms.ChoiceField(
        choices=Question.ANSWER_TYPE_CHOICES,
        widget=forms.Select(attrs={'class':'form-control'}),
        required=True,
        label=u"답변 유형을 선택해 주세요."
    )
    correct = forms.CharField(
        max_length=2000,
        widget=forms.TextInput(attrs={'class':'form-control'}),
        required=True,
        label=u"정답을 적어 주세요."
    )

    class Meta:
        model=Question
        fields=[
            'level', 'question_type', 'title', 'text', 'limit_time', 'answer_type', 'correct'
        ]



class QuestionExampleForm(forms.ModelForm):
    ex_sentence_1 = forms.CharField(max_length=100,
                                    required=False,
                                    widget=forms.TextInput(attrs={'class':'form-control'}),
                                    label=u"보기(a)를 입력하세요.")
    ex_sentence_2 = forms.CharField(max_length=100,
                                    required=False,
                                    widget=forms.TextInput(attrs={'class':'form-control'}),
                                    label=u"보기(b)를 입력하세요.")
    ex_sentence_3 = forms.CharField(max_length=100,
                                    required=False,
                                    widget=forms.TextInput(attrs={'class':'form-control'}),
                                    label=u"보기(c)를 입력하세요.")
    ex_sentence_4 = forms.CharField(max_length=100,
                                    required=False,
                                    widget=forms.TextInput(attrs={'class':'form-control'}),
                                    label=u"보기(d)를 입력하세요.")
    ex_sentence_5 = forms.CharField(max_length=100,
                                    required=False,
                                    widget=forms.TextInput(attrs={'class':'form-control'}),
                                    label=u"보기(e)를 입력하세요.")
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
        widget=forms.Textarea(attrs={'rows':'4', 'class':'form-control'}),
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
        widget=forms.Select(attrs={'class': 'form-control'}),
        label=u"시험 수준을 선택해 주세요."
    )
    title = forms.CharField(
        label=u"시험의 제목을 적어주세요.",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=50
    )
    starting_date = forms.DateTimeField(
        label=u"시험 시작 날짜를 선택해 주세요.",
        required=False,
        widget=forms.DateTimeInput(attrs={'class':'form-control starting_date'})
    )
    closing_date = forms.DateTimeField(
        label=u"시험 마감 날짜를 선택해 주세요.",
        required=False,
        widget=forms.DateTimeInput(attrs={'class': 'form-control closing_date'})
    )
    class Meta:
        model=Quiz
        fields=[
            'level', 'title', 'starting_date', 'closing_date'
        ]


class QuizQuestionForm(forms.ModelForm):
    questions = forms.ModelMultipleChoiceField(
        queryset=Question.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )
    class Meta:
        model=Quiz
        fields=['questions']