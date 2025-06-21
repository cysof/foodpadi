from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CropListingViewSet


router = DefaultRouter()
router.register(r'crops', CropListingViewSet, basename='croplisting')

urlpatterns = [
    path('api/', include(router.urls)),
]
