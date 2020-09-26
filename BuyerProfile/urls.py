from rest_framework.routers import DefaultRouter
from .views import ShippingDetailView

router = DefaultRouter()
router.register(r'shipping', ShippingDetailView)

urlpatterns = router.urls