from django.conf.urls.defaults import *

urlpatterns = patterns('app.main.views',
    url(r'^$', 'index', name='index'),
    url(r'^category/(?P<pk>[\d]+)/$', 'category', name='category'),
    url(r'^test/(?P<pk>[\d]+)/$', 'test', name='test'),
    url(r'^questions/(?P<test_pk>[\d]+)/$', 'questions', name='questions'),
    url(r'^start/(?P<pk>[\d]+)/$', 'start', name='start'),
    url(r'^run/$', 'run', name='run'),
    url(r'^end/$', 'end', name='end'),
    url(r'^answer/$', 'answer', name='answer'),
    url(r'^passed/$', 'passed', name='passed'),
    url(r'^result/(?P<pk>[\d]+)/$', 'result', name='result'),
)