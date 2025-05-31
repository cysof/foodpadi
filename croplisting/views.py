from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticated
from .models import CropListing
from .serializers import CropListingSerializer

class CropListingViewSet(viewsets.ModelViewSet):
    queryset = CropListing.objects.all().order_by('-created_at')
    serializer_class = CropListingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Optionally filters the queryset to show only the authenticated user's listings,
        or all listings depending on user role.
        """
        user = self.request.user
        if user.account_type == 'FARMER':
            return self.queryset.filter(farmer=user)
        return self.queryset

    def perform_create(self, serializer):
        """
        Automatically set the farmer to the logged-in user.
        """
        serializer.save(farmer=self.request.user)
