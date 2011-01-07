# -*- coding: utf-8 -*-
from django import forms
from models import Question, Test, Answer, AnswerResult, AnswerChoice, TestPass
from django.utils.itercompat import is_iterable
from django.conf import settings
import os
from lib.docx import opendocx, nsprefixes
from lxml import etree

class StartTest(forms.ModelForm):
    
    class Meta:
        model = TestPass
        fields = ('mode', 'random_answer_choices')

class TestAdminForm(forms.ModelForm):
    file = forms.FileField(required=False)
    
    class Meta:
        model = Test
        
    def save(self, commit=True):
        test = super(TestAdminForm, self).save(False)
        file = self.cleaned_data['file']

        if file:
            test.save()
            AnswerResult.objects.filter(answer__question__test=test).delete()
            AnswerChoice.objects.filter(question__test=test).delete()
            TestPass.objects.filter(test=test).delete()
            Answer.objects.filter(question__test=test).delete()
            Question.objects.filter(test=test).delete()
            
            doc = opendocx(file)
            questions = []
            for p in doc.xpath('/w:document/w:body/w:p', namespaces=nsprefixes):
                data = {
                    'question': u'',
                    'answers': []
                }
                for r in p.xpath('w:r/w:t', namespaces=nsprefixes):
                    text = r.text.strip()
                    underline = bool(r.getparent().xpath('w:rPr/w:u', namespaces=nsprefixes))
                    if text.startswith(u'►'):
                        data['answers'].append({
                            'text': text,
                            'correct': underline
                        })
                    else:
                        if not data['answers']:
                            data['question'] += ' %s' % text
                        else:
                            data['answers'][-1]['text'] += ' %s' % text
                            if underline:
                                data['answers'][-1]['correct'] = True
                            
                if data['answers']:
                    questions.append(data)
                        
            for question in questions:
                q = Question(test=test, question=question['question'])
                q.save()
                for answer in question['answers']:
                    a = Answer(question=q)
                    a.answer = answer['text']
                    a.correct = answer['correct']
                    a.save()
        return test

class AnswerTestForm(forms.Form):
    answer = forms.ModelMultipleChoiceField(queryset=Question.objects.all(), label='')
    
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
        #if question.multi_answer():
        #    self.fields['answer'].widget = forms.CheckboxSelectMultiple(choices=self.fields['answer'].widget.choices)
        #else:
        #    self.fields['answer'].widget = forms.RadioSelect(choices=self.fields['answer'].widget.choices)
    
    def clean(self):
        data = self.cleaned_data

        if self.test_pass.is_strict() and 'answer' in self.cleaned_data and \
            not self.question.check_answers(self.get_answer()):
            raise forms.ValidationError(u'Не верный ответ, попробуйте снова.')
        
        return data
    
    def get_answer(self):
        a = self.cleaned_data['answer']
        if not is_iterable(a):
            a = [a]
        return a