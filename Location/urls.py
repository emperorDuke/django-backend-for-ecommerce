from rest_framework import routers
from .views import LocationView

router = routers.DefaultRouter()
router.register(r'locations', LocationView)

urlpatterns = router.urls