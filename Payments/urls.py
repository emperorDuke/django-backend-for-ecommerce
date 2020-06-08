from django.urls import re_path

from .views import CouponView

urlpatterns = [
    re_path(r'^order/(?P<order_pk>[0-9]+)/coupon/$', CouponView.as_view(), name='coupon-view')
]