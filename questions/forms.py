from django import forms

class CreateQuestions(forms.Form):
    question_form = forms.CharField(label='question', max_length=2500)
    day_form = forms.DateTimeField(label='date')

class CreateAnswers(forms.Form):
    answer = forms.CharField(label='answer')