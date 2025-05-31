from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated  # Optional - depends on your auth setup
from .models import FarmPadiUser, Profile
from .serializers import FarmPadiUserSerializer, ProfileSerializer

class FarmPadiUserViewSet(viewsets.ModelViewSet):
    queryset = FarmPadiUser.objects.all()
    serializer_class = FarmPadiUserSerializer
    permission_classes = [IsAuthenticated]

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]  