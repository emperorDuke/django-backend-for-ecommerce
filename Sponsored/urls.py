from django.urls import re_path, include

from rest_framework.routers import DefaultRouter
from .views import SponsoredProductViewset, SponsoredStoreViewset


router = DefaultRouter()

router.register(r'products', SponsoredProductViewset)
router.register(r'stores', SponsoredStoreViewset)

urlpatterns = [
    re_path(r'^sponsored/', include(router.urls))
]