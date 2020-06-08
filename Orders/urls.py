from django.urls import re_path, include
from rest_framework.routers import DefaultRouter

from .views import OrderView


router = DefaultRouter()

router.register(r'order', OrderView)


urlpatterns = [
    re_path(r'^', include(router.urls))
]