from django.urls import re_path

from .views import AdminAdvertView


urlpatterns = [
    re_path(r'^admin-adverts/$', AdminAdvertView.as_view(), name='list-admin-adverts')
]