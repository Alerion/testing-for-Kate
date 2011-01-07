# -*- coding: utf-8 -*-
from django import template
from app.main.models import Category

register = template.Library()

@register.inclusion_tag('main/side_tests.html')
def tests():
    
    return {
        'items': Category.objects.all()
    }

@register.inclusion_tag('main/side_lectures.html')
def lectures():
    
    return {
        'items': Category.objects.all()
    }

@register.inclusion_tag('statistic/side_statistic.html')
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