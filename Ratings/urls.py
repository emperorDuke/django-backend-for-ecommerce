from django.urls import re_path

from . import views

urlpatterns = [
    re_path(r'^stores/(?P<pk>[0-9]+)/rating/$', views.StoreRatingView.as_view(), name='store_rating'),
    re_path(r'^products/(?P<pk>[0-9]+)/rating/$', views.ProductRatingView.as_view(), name='product_rating')
]

