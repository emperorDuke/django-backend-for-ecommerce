from django.urls import re_path

from .views import LocationView


urlpatterns = [
    re_path(r'^location/$', LocationView.as_view(), name='get-location')
]