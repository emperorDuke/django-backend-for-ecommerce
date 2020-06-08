from django.urls import include,re_path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()

router.register(r'adverts', views.Advert_view, base_name='adverts')


urlpatterns = [
    re_path(r'^', include(router.urls))
]

