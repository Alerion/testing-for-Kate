# -*- coding: utf-8 -*-
from django import forms
from models import Question, Test, Answer, AnswerResult, AnswerChoice, TestPass
from django.utils.itercompat import is_iterable
from lib.docx import opendocx, nsprefixes
from app.main.parser import parser
from copy import copy

class StartTest(forms.ModelForm):
    
    class Meta:
        model = TestPass
        fields = ('mode', 'random_answer_choices')

class TestAdminForm(forms.ModelForm):
    file = forms.FileField(required=False)
    questions_count = forms.IntegerField(required=False, help_text=u'Количество вопросов в тесте. Оставьте пустым если не хотите разбивать вопросы на несколько тестов', 
                                   label=u'Кол.вопросов')
    
    class Meta:
        model = Test
        
    def save(self, commit=True):
        test = super(TestAdminForm, self).save(False)
        file = self.cleaned_data['file']
        questions_count = self.cleaned_data['questions_count']
        
        if file:
            test_name = test.name
            test.save()
            AnswerResult.objects.filter(answer__question__test=test).delete()
            AnswerChoice.objects.filter(question__test=test).delete()
            TestPass.objects.filter(test=test).delete()
            Answer.objects.filter(question__test=test).delete()
            Question.objects.filter(test=test).delete()
            
            questions = parser(file)
            count = 0
            cur_test = test
            
            for i, question in enumerate(questions):
                count += 1
                q = Question(test=cur_test, question=question['question'])
                if question['text_answer']:
                    q.text_answer = question['text_answer']
                    q.save()
                else:
                    q.save()
                    for answer in question['answers']:
                        a = Answer(question=q)
                        a.answer = answer['text']
                        a.correct = answer['correct']
                        a.save()
                
                if questions_count and count >= questions_count:
                    if (len(questions) - i) >= questions_count:
                        cur_test.name = '%s [%s-%s]' % (test_name, i+1-count, i+1)
                        cur_test.save()                           
                        cur_test = copy(test)
                        cur_test.pk = None
                        cur_test.save()
                    else:
                        cur_test.name = '%s [%s-%s]' % (test_name, i+1-count, len(questions))
                        cur_test.save()
                                                      
                    count = 0
                
        return test

class AnswerTestForm(forms.Form):
    answer = forms.ModelMultipleChoiceField(queryset=Question.objects.all(), label='', required=False)
    text_answer = forms.CharField(required=False, label=u'Введите ответ')
    
    def __init__(self, question, test_pass, *args, **kwargs):
        self.question = question
        self.test_pass = test_pass
        #if question.multi_answer():
        #    self.base_fields['answer'] = forms.ModelMultipleChoiceField(queryset=question.answer_set.order_by('?'))
        #else:
        #    self.base_fields['answer'] = forms.ModelChoiceField(queryset=question.answer_set.order_by('?'), empty_label=None, label='')
        
        if test_pass.random_answer_choices:
            self.base_fields['answer'].queryset = question.answer_set.order_by('?')
        else:
            self.base_fields['answer'].queryset = question.answer_set.all()
        
        super(AnswerTestForm, self).__init__(*args, **kwargs)
        
        self.fields['answer'].widget = forms.CheckboxSelectMultiple(choices=self.fields['answer'].widget.choices)
        
        if not question.text_answer:
            self.fields['text_answer'].widget = forms.HiddenInput()
            
        #if question.multi_answer():
        #    self.fields['answer'].widget = forms.CheckboxSelectMultiple(choices=self.fields['answer'].widget.choices)
        #else:
        #    self.fields['answer'].widget = forms.RadioSelect(choices=self.fields['answer'].widget.choices)
    
    def clean(self):
        data = self.cleaned_data
        
        if not data['text_answer'] and not data['answer']:
            #TODO: set error to one of field depending from self.question.text_answer
            raise forms.ValidationError('Введите ответ')
        
        if self.test_pass.is_strict() and 'answer' in self.cleaned_data and \
            not self.question.check_answers(self.get_answer()):
            raise forms.ValidationError(u'Не верный ответ, попробуйте снова.')
        
        return data
    
    def get_answer(self):
        if self.question.text_answer:
            return unicode(self.cleaned_data['text_answer']).strip()
        
        a = self.cleaned_data['answer']
        if not is_iterable(a):
            a = [a]
        return a