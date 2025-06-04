from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FarmPadiUserViewSet, ProfileViewSet
from rest_framework_simplejwt.views import TokenRefreshView
from . import views


router = DefaultRouter()
router.register(r'users', FarmPadiUserViewSet)
router.register(r'profiles', ProfileViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    
    path('api/register/', views.UserRegistrationView.as_view(), name='register'),
    path('api/login/', views.CustomTokenObtainPairView.as_view(), name='login'),
    path('api/logout/', views.LogoutView.as_view(), name='logout'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    path('api/profile/', views.UserProfileView.as_view(), name='profile'),
    path('api/change-password/', views.ChangePasswordView.as_view(), name='change_password'),
]
