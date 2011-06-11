# -*- coding: utf-8 -*-
from lib import render_to, JSONResponse
from django.shortcuts import redirect
from app.main.models import Category, Test, TestPass, AnswerChoice, AnswerResult, Question
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from forms import AnswerTestForm, StartTest
from django.http import HttpResponse
from django.views.generic.list_detail import object_list 
import datetime
from copy import deepcopy

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
    current_test = request.current_test
    if not current_test:
        return redirect('/')   
    if current_test.is_end():
        return redirect('main:end')
    form = AnswerTestForm(current_test.first_question, current_test)
    return {
        'form': form,
        'question': current_test.first_question
    }

@login_required
@render_to('main/answer.html')
def answer(request):
    if not request.current_test:
        return redirect('/') 
    if request.current_test.is_end():
        return HttpResponse('END')
    current_test = request.current_test
    form = AnswerTestForm(current_test.first_question, current_test, request.POST)
    prev_answer = None
    if form.is_valid():
        answers = form.get_answer()
        question = current_test.first_question
        ac = AnswerChoice(question=question, test_pass=current_test)
        ac.save()
        if question.text_answer:
            ac.text_answer = answers
            ac.save()
        else:
            for item in answers:
                AnswerResult(question=ac, answer=item).save()
        if not current_test.first_question:
            return HttpResponse('END')
        if current_test.is_simple():
            prev_answer = ac
        form = AnswerTestForm(current_test.first_question, current_test)        
    return {
        'form': form,
        'prev_answer': prev_answer,
        'question': current_test.first_question
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
    return {
        'obj': obj
    }

@login_required    
def copy(request):
    user = request.user
    if not user.is_active and user.is_superuser:
        return JSONResponse({'error': 'У вас не хватает прав доступа'})
    
    try:
        test = Test.objects.get(pk=request.POST.get('test'))
    except (Test.DoesNotExist, TypeError, ValueError):
        return JSONResponse({'error': 'Не могу скопировать в несуществуюущий тест'})
    
    try:
        question = Question.objects.get(pk=request.POST.get('question'))
    except (Question.DoesNotExist, TypeError, ValueError):
        return JSONResponse({'error': 'Не могу скопировать несуществуюущий вопрос'})    
    
    if Question.objects.filter(test=test, question=question.question).exists():
        return JSONResponse({'error': 'Такой вопрос уже есть в тесте'})
    
    new_question = deepcopy(question)
    new_question.pk = None
    new_question.test = test
    new_question.save()
    
    for answer in question.answer_set.all():
        new_answer = deepcopy(answer)
        new_answer.pk = None
        new_answer.question = new_question
        new_answer.save()
        
    response = JSONResponse({})
    max_age = 365*24*60*60
    expires = datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age), "%a, %d-%b-%Y %H:%M:%S GMT")
    response.set_cookie('last_test_copy_to', test.pk, max_age=max_age, expires=expires)
    return response