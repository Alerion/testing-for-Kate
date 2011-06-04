# -*- coding: utf-8 -*-
from django.db import models
from app.account.models import User
from datetime import datetime, timedelta

GRADES = (
    (0.85, 5),
    (0.65, 4),
    (0.45, 3),
    (0, 2),
)

class Lecture(models.Model):
    title = models.CharField(u'Название', max_length=200)
    annotation = models.TextField(u'Аннотация')
    content = models.TextField(u'Содержание', blank=True)
    category = models.ForeignKey('Category', verbose_name=u'категория')
    
    class Meta:
        verbose_name = u'лекцию'
        verbose_name_plural = u'лекции'
    
    def __unicode__(self):
        return self.title        

    @models.permalink
    def get_absolute_url(self):
        return ('lectures:lecture', (), {'pk': self.pk})

class Category(models.Model):
    name = models.CharField(u'название', max_length=255)
    
    class Meta:
        verbose_name = u'категорию'
        verbose_name_plural = u'категории'
    
    def __unicode__(self):
        return self.name
    
    @models.permalink
    def get_absolute_url(self):
        return ('main:category', (), {'pk': self.pk})
    
class Test(models.Model):
    HARD = 1
    NORMAL = 2
    EASY = 3
    
    CHOICES = (
        (HARD, u'эксперт'),
        (NORMAL, u'средний уровень'),
        (EASY, u'основы')
    )
    
    name = models.CharField(u'название', max_length=255)
    time = models.PositiveIntegerField(u'время', help_text=u'время на выполнение в мин.')
    difficulty = models.IntegerField(u'сложность', choices=CHOICES, default=NORMAL)
    category = models.ForeignKey(Category, verbose_name=u'категория')
    description = models.TextField(u'Описание', blank=True)
    
    class Meta:
        verbose_name = u'тест'
        verbose_name_plural = u'тесты'
    
    def __unicode__(self):
        return '%s(%s)' % (self.name, self.get_difficulty_display())
 
    @models.permalink
    def get_absolute_url(self):
        return ('main:test', (), {'pk': self.pk})
    
class Question(models.Model):
    test = models.ForeignKey(Test, verbose_name=u'тест')
    question = models.CharField(u'Вопрос', max_length=500)
    extra = models.CharField(u'Дополнительно', max_length=500, blank=True)

    class Meta:
        verbose_name = u'вопрос'
        verbose_name_plural = u'вопросы'
    
    def __unicode__(self):
        return self.question
    
    def multi_answer(self):
        return self.correct_count() > 1
    
    def correct_count(self):
        return self.answer_set.filter(correct=True).count()
    
    def check_answers(self, answers):
        correct = 0
        incorrect = 0
        for item in answers:
            if item.correct:
                correct += 1
            else:
                incorrect += 1
        return correct >= self.correct_count() and not incorrect
    
class Answer(models.Model):
    question = models.ForeignKey(Question, verbose_name=u'вопрос')
    answer = models.CharField(u'ответ', max_length=500)
    correct = models.BooleanField(u'верный?', default=False)
    #count = models.PositiveIntegerField(default=0, editable=False)

    class Meta:
        verbose_name = u'ответ'
        verbose_name_plural = u'ответы'
    
    def __unicode__(self):
        return self.answer
    
class TestPass(models.Model):
    SIMPLE = 1
    STRICT = 2
    MODE_CHOICES = (
        (SIMPLE, u'Обычный'),
        (STRICT, u'Обязательный')
    )
    test = models.ForeignKey(Test)
    user = models.ForeignKey(User)
    start = models.DateTimeField(auto_now_add=True)
    complite = models.BooleanField(default=False, editable=False)
    result = models.FloatField(default=0)
    mode = models.IntegerField(u'Режим', choices=MODE_CHOICES, default=SIMPLE, 
                               help_text=u'Обязательный - вопрос не считаеться засчитаным, пока не будет получен верный ответ.')
    random_answer_choices = models.BooleanField(u'Случайные варианты ответов', default=False)
    
    def __unicode__(self):
        return '%s' % self.test.__unicode__()
    
    def is_simple(self):
        return self.mode == self.SIMPLE
    
    def is_strict(self):
        return self.mode == self.STRICT
    
    @property
    def grade(self):
        for item in GRADES:
            if self.result > item[0]:
                return item[1]
            grade = item
        return grade[1]

    @models.permalink
    def get_absolute_url(self):
        return ('main:run', (), {})
    
    def is_end(self):
        t = self.start + timedelta(minutes=self.test.time)
        if t < datetime.now():
            return True
        if not self.first_question:
            return True
        return False
    
    def count_result(self):
        questions_count = self.questions.count()
        if questions_count:
            self.result = float(self.correct_answers()) / float(questions_count)
        else:
            self.result = 0
    
    def correct_answers(self):
        answers = self.answerchoice_set.all()
        correct = 0
        for item in answers:
            if item.correct:
                correct += 1
        return correct
    
    @property
    def left_time(self):
        t = self.start + timedelta(minutes=self.test.time) - datetime.now()
        if t > timedelta():
            return t
        return timedelta()
    
    @property
    def questions(self):
        return self.test.question_set.all()
    
    @property
    def answered_questions(self):
        return [item.question for item in self.answerchoice_set.all()]
    
    @property
    def first_question(self):
        answered = self.answered_questions
        for item in self.questions:
            if not item in answered:
                return item 
    
class AnswerChoice(models.Model):
    question = models.ForeignKey(Question)
    test_pass = models.ForeignKey(TestPass)
    
    def missed_correct(self):
        answers_pks = [item.answer_id for item in self.answers.all()]
        return self.question.answer_set.filter(correct=True).exclude(pk__in=answers_pks)
    
    @property
    def correct(self):
        correct = 0
        incorrect = 0
        for item in self.answers.all():
            if item.answer.correct:
                correct += 1
            else:
                incorrect += 1
        return correct >= self.question.correct_count() and not incorrect
    
class AnswerResult(models.Model):
    question = models.ForeignKey(AnswerChoice, related_name='answers')
    answer = models.ForeignKey(Answer)
    
    @property
    def correct(self):
        return self.answer.correct
    