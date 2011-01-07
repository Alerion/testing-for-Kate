from django.conf.urls.defaults import *

urlpatterns = patterns('app.statistic.views',
    url(r'^$', 'index', name='index'),
    url(r'^discipline/$', 'discipline_main', name='discipline_main'),
    url(r'^pass/discipline/$', 'pass_discipline', name='pass_discipline_main'),
    url(r'^discipline/(?P<pk>[\d]+)/$', 'discipline', name='discipline'),
)