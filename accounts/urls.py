from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FarmPadiUserViewSet, ProfileViewSet

router = DefaultRouter()
router.register(r'users', FarmPadiUserViewSet)
router.register(r'profiles', ProfileViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
