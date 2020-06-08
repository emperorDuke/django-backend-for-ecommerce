from django.urls import include, re_path

from rest_framework import routers

from .views import StoreView

router = routers.DefaultRouter()

router.register(r'stores', StoreView)



urlpatterns = [
    re_path(r'^', include(router.urls))
]

