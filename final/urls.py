# coding=utf-8

from django.conf.urls import url

from . import views

urlpatterns=[url(r'^final',views.weixin,name='weixin'),
             url(r'^test', views.test, name='test')]