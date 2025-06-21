from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import CropListing
from .serializers import CropListingSerializer
from .permissions import CropListingPermission
from django.utils.dateparse import parse_date
from rest_framework.exceptions import PermissionDenied


class CropListingViewSet(viewsets.ModelViewSet):
    serializer_class = CropListingSerializer
    queryset = CropListing.objects.all().order_by('-created_at')
    permission_classes = [CropListingPermission]

    def perform_create(self, serializer):
        user = self.request.user
        if not user.is_authenticated:
            raise PermissionDenied("Authentication required.")
        if user.account_type != 'FARMER':
            raise PermissionDenied("Only farmers can create crop listings.")
        serializer.save(farmer=user)


    def get_queryset(self):
        """
        Supports filtering by crop_name, location, harvested_date, etc.
        """
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
