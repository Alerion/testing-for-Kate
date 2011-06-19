# -*- coding: utf-8 -*-
from django.contrib import admin
from models import Category, Test, Question, Answer, Lecture
from forms import TestAdminForm

class LectureAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)
    
admin.site.register(Lecture, LectureAdmin)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    
admin.site.register(Category, CategoryAdmin)

class TestAdmin(admin.ModelAdmin):
    form = TestAdminForm
    list_display = ('name', 'category', 'difficulty', 'time')
    filter_fields = ('category',)
    search_fields = ('name',)
    
admin.site.register(Test, TestAdmin)

class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 5

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question', 'test')
    filter_fields = ('test',)
    search_fields = ('question',)
    inlines = [AnswerInline]
    
admin.site.register(Question, QuestionAdmin)
    
