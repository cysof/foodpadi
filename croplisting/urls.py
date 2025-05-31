from rest_framework.routers import DefaultRouter
from .views import CropListingViewSet

router = DefaultRouter()
router.register(r'crop-listings', CropListingViewSet, basename='crop-listing')

urlpatterns = router.urls
