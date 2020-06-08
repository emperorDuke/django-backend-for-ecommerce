from django.urls import re_path
from . import views


urlpatterns = [
    re_path(r'^stores/(?P<storePk>[0-9]+)/review/$', views.StorePostReview.as_view(), name='store_post_review'),
    re_path(r'^stores/(?P<storePk>[0-9]+)/reviews/$', views.StoreGetReview.as_view(), name='store_get_review'),
    re_path(r'^stores/review/(?P<reviewPk>[0-9]+)/$', views.StoreRespondToReview.as_view(), name='store_respond_to_review'),
    re_path(r'^products/(?P<productPk>[0-9]+)/review/$', views.ProductPostReview.as_view(), name='product_post_review'),
    re_path(r'^products/(?P<productPk>[0-9]+)/reviews/$', views.ProductGetReview.as_view(), name='product_get_review'),
    re_path(r'^products/review/(?P<reviewPk>[0-9]+)/$', views.ProductRespondToReview.as_view(), name='product_respond_to_review')
]