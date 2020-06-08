from django.urls import re_path

from . import views

urlpatterns = [
    re_path(r'^categories/$', views.CategoryView.as_view(), name='catgory view'),
    re_path(r'^category/filters/(?P<name>[A-Za-z0-9]+)/$', views.FilterView.as_view(), name='filter keys')
]

