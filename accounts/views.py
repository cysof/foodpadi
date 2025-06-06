from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import FarmPadiUser, Profile
from .serializers import FarmPadiUserSerializer, ProfileSerializer
from .serializers import FarmPadiUserRegistrationSerializer

from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.db import transaction
from rest_framework import serializers
from .serializers import CustomTokenObtainPairSerializer

class FarmPadiUserViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing FarmPadiUser instances.
    """
    queryset = FarmPadiUser.objects.all()
    serializer_class = FarmPadiUserSerializer
    permission_classes = [IsAuthenticated]

class ProfileViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing Profile instances.
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]  

class UserRegistrationView(generics.CreateAPIView):
    """
    A view for registering new users.
    """
    queryset = FarmPadiUser.objects.all()
    serializer_class = FarmPadiUserRegistrationSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        """
        Create a new user instance.
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            # Generate tokens for the new user
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'message': 'Account created successfully!',
                'user': FarmPadiUserSerializer(user).data,
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    A view for obtaining a token pair.
    """
    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        """
        Obtain a token pair.
        """
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            return Response({
                'message': 'Login successful',
                **serializer.validated_data
            }, status=status.HTTP_200_OK)
        except serializers.ValidationError as e:
            return Response({
                'error': 'Login failed',
                'details': e.detail
            }, status=status.HTTP_401_UNAUTHORIZED)



class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    A view for retrieving and updating the user's profile.
    """
    serializer_class = FarmPadiUserSerializer
    
    def get_object(self):
        """
        Get the user's profile.
        """
        return self.request.user

    def update(self, request, *args, **kwargs):
        """
        Update the user's profile.
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Profile updated successfully',
                'user': serializer.data
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    """
    A view for logging out.
    """
    def post(self, request):
        """
        Log out.
        """
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({
                'message': 'Logout successful'
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'error': 'Invalid token'
            }, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(APIView):
    """
    A view for changing the user's password.
    """
    def post(self, request):
        """
        Change the user's password.
        """
        user = request.user
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        
        if not user.check_password(old_password):
            return Response({
                'error': 'Old password is incorrect'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if len(new_password) < 8:
            return Response({
                'error': 'New password must be at least 8 characters long'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        user.set_password(new_password)
        user.save()
        
        return Response({
            'message': 'Password changed successfully'
        }, status=status.HTTP_200_OK)