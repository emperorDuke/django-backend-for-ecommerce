from django.urls import re_path, include

from rest_framework import routers

from .views import CartView

router = routers.DefaultRouter()

router.register(r'cart', CartView)

urlpatterns = [
    re_path(r'^', include(router.urls))
]