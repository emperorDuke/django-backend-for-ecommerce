from django.urls import re_path, include

from rest_framework import routers

from .views import ProductViewset, AttributeView, ProductMetaView


router = routers.DefaultRouter()

router.register(r'products', ProductViewset)

urlpatterns = [
    re_path(r'^products/attributes/$', AttributeView.as_view({'post': 'create'}), name='create_attributes'),
    re_path(r'^products/attributes/(?P<pk>[0-9]+)/$', AttributeView.as_view({'patch': 'partial_update'}), name='update_attributes'),
    re_path(r'^products/(?P<pk>[0-9]+)/attributes/$', AttributeView.as_view({'get': 'retrieve'}), name='retrieve'),
    re_path(r'^products/meta/$', ProductMetaView.as_view({'post': 'create'}), name='create_meta'),
    re_path(r'^products/(?P<pk>[0-9]+)/meta/$', ProductMetaView.as_view({'patch': 'partial_update'}), name='update_meta'),
    re_path(r'^products/(?P<pk>[0-9]+)/meta/s/$', ProductMetaView.as_view({'get': 'retrieve'}), name='retrieve_meta'),
    re_path(r'^', include(router.urls))
]

