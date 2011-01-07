# -*- coding: utf-8 -*-
from lib import render_to
from django.shortcuts import redirect
from app.main.models import Category, Test, TestPass, AnswerChoice, AnswerResult
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from forms import AnswerTestForm, StartTest
from django.http import HttpResponse
from django.views.generic.list_detail import object_list 

@render_to('main/index.html')
def index(request):
    #request.current_test.get_absolute_url()
    return {
        'categories': Category.objects.select_related().all()
    }

@render_to('main/category.html')    
def category(request, pk):
    obj = get_object_or_404(Category, pk=pk)
    return {
        'obj': obj
    }

@render_to('main/test.html')
def test(request, pk):
    obj = get_object_or_404(Test, pk=pk)
    return {
        'obj': obj
    }

def questions(request, test_pk):
    test = get_object_or_404(Test, pk=test_pk)
    qs = test.question_set.all()
    context = {
        'test': test
    }
    return object_list(request, queryset=qs,
                       paginate_by=30,
                       template_name='main/questions.html',
                       template_object_name='question',
                       extra_context=context)    
    
@login_required
@render_to('main/start.html')    
def start(request, pk):
    if request.current_test:
        return {}
    obj = get_object_or_404(Test, pk=pk)
    
    form = StartTest(request.POST or None)
    if form.is_valid():
        test_pass = form.save(False)
        test_pass.user = request.user
        test_pass.test = obj
        test_pass.save()
        return redirect(test_pass.get_absolute_url())
    return {
        'form': form
    }

@login_required
@render_to('main/run.html')
def run(request):
    if not request.current_test:
        return redirect('/')   
    if request.current_test.is_end():
        return redirect('main:end')
    form = AnswerTestForm(request.current_test.first_question, request.current_test)
    return {
        'form': form
    }

@login_required
@render_to('main/answer.html')
def answer(request):
    if not request.current_test:
        return redirect('/') 
    if request.current_test.is_end():
        return HttpResponse('END')
    form = AnswerTestForm(request.current_test.first_question, request.current_test, request.POST)
    prev_answer = None
    if form.is_valid():
        answers = form.get_answer()
        ac = AnswerChoice(question=request.current_test.first_question, test_pass=request.current_test)
        ac.save()
        for item in answers:
            AnswerResult(question=ac, answer=item).save()
        if not request.current_test.first_question:
            return HttpResponse('END')
        if request.current_test.is_simple():
            prev_answer = ac
        form = AnswerTestForm(request.current_test.first_question, request.current_test)        
    return {
        'form': form,
        'prev_answer': prev_answer
    }

@login_required
@render_to('main/end.html')
def end(request):
    if not request.current_test:
         return redirect('/')
    request.current_test.complite = True
    request.current_test.count_result()
    request.current_test.save()
    return redirect('main:result', pk=request.current_test.pk)

@login_required
@render_to('main/passed.html')
def passed(request):
    items = TestPass.objects.filter(user=request.user)
    return {
        'items': items
    }

@login_required
@render_to('main/result.html')
def result(request, pk):
    obj = get_object_or_404(TestPass, pk=pk, user=request.user)
    obj.count_result()
    print obj.result
    return {
        'obj': obj
    }