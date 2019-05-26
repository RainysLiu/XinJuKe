from django.conf.urls import url, include
from django.core.paginator import Paginator
from django.shortcuts import render


from house.models import *
from user import views
urlpatterns = [
    url(r'^register/$', views.register),
    url(r'^register_handle/$', views.register_handle),
    url(r'^register_exist/$',views.register_exist),
    url(r'^register_tel_exist/$',views.register_tel_exist),
    url(r'^login/$', views.login),
    url(r'^login_handle/$', views.login_handle),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^info/$', views.info),
    url(r'^marked/$', views.marked),
    url(r'^mypublish/$', views.published),
    url(r'^collection/(\d+)/$', views.collection),
    url(r'^modifyinfo/$', views.modifyinfo),
    url(r'^modifyinfo_handle/$', views.modifyinfo_handle),
    url(r'^update_img/$', views.upload_userimg),
]