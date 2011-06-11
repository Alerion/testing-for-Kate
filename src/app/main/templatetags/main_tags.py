# -*- coding: utf-8 -*-
from django import template
from app.main.models import Category, Test

register = template.Library()

@register.inclusion_tag('main/_copy_question.html', takes_context=True)
def copy_question(context, question):
    test = question.test
    context['copy_choices'] = Test.objects.exclude(pk=test.pk) \
        .filter(category=test.category)
    context['copy_question_id'] = question.pk
    try:
        context['last_test_copy_to'] = int(context['request'].COOKIES.get('last_test_copy_to'))
    except (TypeError, ValueError):
        context['last_test_copy_to'] = None
    return context

@register.inclusion_tag('main/_side_tests.html')
def tests():
    
    return {
        'items': Category.objects.all()
    }

@register.inclusion_tag('main/_side_lectures.html')
def lectures():
    
    return {
        'items': Category.objects.all()
    }

@register.inclusion_tag('statistic/_side_statistic.html')
def statistic():
    
    return {
        
    }

def timedelta(value):
    seconds = value.seconds
    s = seconds % 60
    m = seconds % 3600 // 60
    h = seconds // 3600 + value.days * 24
    return '%02d:%02d:%02d' % (h, m, s)

register.filter('timedelta', timedelta)

def percent(value):
    value = int(round(value, 2)*100)
    return '%s%%' % value

register.filter('percent', percent)