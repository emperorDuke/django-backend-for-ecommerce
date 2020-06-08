from django.contrib import admin


from .models.storeReviews import StoreReview
from .models.storeReviewResponse import StoreResponse
from .models.productReviews import ProductReview
from .models.productReviewResponse import ProductReviewResponse


admin.site.register(StoreReview)
admin.site.register(StoreResponse)
admin.site.register(ProductReview)
admin.site.register(ProductReviewResponse)

