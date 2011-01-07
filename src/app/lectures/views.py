# -*- coding: utf-8 -*-
from lib import render_to
from app.main.models import Lecture, Category
from django.shortcuts import get_object_or_404

@render_to('lectures/index.html')
def index(request):
    return {
        'categories': Category.objects.all()
    }

@render_to('lectures/category.html')    
def category(request, pk):
    obj = get_object_or_404(Category, pk=pk)
    return {
        'obj': obj
    }

@render_to('lectures/lecture.html')    
def lecture(request, pk):
    obj = get_object_or_404(Lecture, pk=pk)
    return {
        'obj': obj
    }