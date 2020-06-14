from django.conf.urls import url, include
from django.core.paginator import Paginator
from django.shortcuts import render


from order import views

urlpatterns = [
    url(r"^myorder/$", views.order),
    url(r"^addorder/(\d+)/(\d+)/$", views.addorder),
]
