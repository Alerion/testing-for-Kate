# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings
from patch import sites_flatpages_patch

admin.autodiscover()
sites_flatpages_patch()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'^registration/', include('registration.urls')),
    url(r'^login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout'),    
    (r'^', include('app.main.urls',  namespace='main')),
    (r'^lectures/', include('app.lectures.urls',  namespace='lectures')),
    (r'^statistic/', include('app.statistic.urls',  namespace='statistic')),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)