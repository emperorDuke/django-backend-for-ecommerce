from django.urls import include, re_path

from rest_framework import routers

from . import views

router = routers.DefaultRouter()

router.register(r'users', views.UserViewSet)

urlpatterns = [
    re_path(r'^confirm_password/$', views.ConfirmPassword.as_view(),
            name='confirm_password'),
    re_path(r'^change_password/(?P<pk>[0-9]+)&(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
            views.ChangePassword.as_view(), name='change_password'),
    re_path(r'^forgot_password/$', views.ForgotPassword.as_view(),
            name='forgot_password'),
    re_path(
        r'^confirm_link/(?P<uidb64>[0-9A-Za-z_\-]+)&(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.ConfirmLink.as_view(), name='confirm_link'),
    re_path(r'^seller/', include((router.urls, 'UserViewSet'), namespace='seller')),
    re_path(r'^buyer/', include((router.urls, 'UserViewSet'), namespace='buyer')),
]
