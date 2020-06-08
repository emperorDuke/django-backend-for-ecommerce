from rest_framework.routers import DefaultRouter
from .views import ShippingDetailView

router = DefaultRouter()
router.register(r'shipping-detail', ShippingDetailView)

urlpatterns = router.urls