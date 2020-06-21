from django.urls import include, re_path

from rest_framework import routers

from .views import StoreView, Advert_view

router = routers.DefaultRouter()

router.register(r'stores', StoreView)
router.register(r'adverts', Advert_view)


urlpatterns = [
    re_path(r'^', include(router.urls))
]

