from rest_framework.routers import DefaultRouter
from .views import ShippingView

router = DefaultRouter()
router.register(r'shipping', ShippingView)

urlpatterns = router.urls