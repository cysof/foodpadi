from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from django.utils.dateparse import parse_date
from .models import CropListing
from .serializers import CropListingSerializer

# ✅ Custom permission class
class CropListingPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        # Allow anyone to view (GET, HEAD, OPTIONS), require login for others
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Only allow editing/deleting by the farmer who owns the listing
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.farmer == request.user

# ✅ Main ViewSet
class CropListingViewSet(viewsets.ModelViewSet):
    serializer_class = CropListingSerializer
    queryset = CropListing.objects.all().order_by('-created_at')
    permission_classes = [IsAuthenticated, CropListingPermission]

    def perform_create(self, serializer):
        user = self.request.user
        if not user.is_authenticated:
            raise PermissionDenied("Authentication required.")
        if user.account_type != 'FARMER':
            raise PermissionDenied("Only farmers can create crop listings.")
        serializer.save(farmer=user)

    def get_queryset(self):
        queryset = CropListing.objects.all().order_by('-created_at')
        params = self.request.query_params

        location = params.get('location')
        crop_name = params.get('crop_name')
        availability = params.get('availability')
        freshness = params.get('harvested_date')
        is_organic = params.get('is_Organic')

        if location:
            queryset = queryset.filter(location__iexact=location)
        if crop_name:
            queryset = queryset.filter(crop_name__iexact=crop_name)
        if availability:
            queryset = queryset.filter(availability__iexact=availability)
        if freshness:
            queryset = queryset.filter(freshness__gt=parse_date(freshness))
        if is_organic is not None:
            queryset = queryset.filter(is_Organic=(is_organic.lower() == 'true'))

        return queryset
