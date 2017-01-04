#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.conf.urls import url
from . import views

urlpatterns = [
    #url(r'^admin/', admin.site.urls),
    url(r'^bloglist/$',views.blog_list,name='bloglist'),
    url(r'^blog/(?P<id>\d+)/$', views.blog_show, name='detailblog'),
    url(r'^blog/tag/(?P<id>\d+)/$',views.blog_filter, name='filtrblog'),
    url(r'^blog/add/$',views.blog_add,name='addblog'),
    url(r'^blog/(?P<id>\w+)/update/$',views.blog_update,name='updateblog'),
    url(r'^blog/(?P<id>\w+)/del/$',views.blog_del,name='delblog')


]