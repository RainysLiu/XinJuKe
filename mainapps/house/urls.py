from django.conf.urls import url, include
from django.core.paginator import Paginator
from django.shortcuts import render


from house.models import *
from house import views

urlpatterns = [
    url(r"^show/(\d+)/", views.show),
    url(r"^search/", views.search),
    url(r"^addhouse/", views.addhouse),
    url(r"^add_handle/", views.add_handle),
    url(r"^upload_img/", views.uploadimg),
]
