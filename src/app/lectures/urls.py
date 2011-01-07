from django.conf.urls.defaults import *

urlpatterns = patterns('app.lectures.views',
    url(r'^$', 'index', name='index'),
    url(r'^(?P<pk>[\d]+)/$', 'lecture', name='lecture'),
    url(r'^category/(?P<pk>[\d]+)/$', 'category', name='category'),    
)