from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticated
from .models import CropListing
from .serializers import CropListingSerializer
from rest_framework.exceptions import PermissionDenied
from django.utils.dateparse import parse_date

class CropListingPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        Check permissions for a specific object.

        Only farmers can create and edit their own crop listings.

        :param request: The request being made.
        :type request: Request
        :param view: The view being used.
        :type view: View
        :param obj: The object being accessed.
        :type obj: CropListing
        :return: Whether the user has permission to access the object.
        :rtype: bool
        """
        
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.farmer == request.user

class CropListingViewSet(viewsets.ModelViewSet):
    serializer_class = CropListingSerializer
    permission_classes = [CropListingPermission]

    def perform_create(self, serializer):
        """
        Automatically set the farmer to the logged-in user.
        """
        if self.request.user.account_type == 'FARMER':
            serializer.save(farmer=self.request.user)
        else:
            raise PermissionDenied("Only farmers can create crop listings")
    
    def get_queryset(self):
        """
        Retrieve a queryset of CropListing objects, optionally filtered by query parameters.

        Filters the queryset based on the query parameters provided in the request:
        - `location`: Filters by exact match of the location.
        - `crop_name`: Filters by exact match of the crop name.
        - `availability`: Filters by exact match of the availability status.
        - `freshness`: Filters for crops harvested after the specified date.
        - `is_Organic`: Filters by organic status, case-insensitive.

        Returns:
            QuerySet: A Django QuerySet of filtered CropListing objects.
        """

        queryset = CropListing.objects.all().order_by('-created_at')
        location =self.request.query_params.get('location')
        freshness =self.request.query_params.get('harvested_date')
        is_Organic =self.request.query_params.get('is_Organic')
        availability = self.request.query_params.get('availability')
        crop_name = self.request.query_params.get('crop_name')
        
        if location:
            queryset = queryset.filter(location__iexact=location)
        if crop_name:
            queryset = queryset.filter(crop_name__iexact=crop_name)
        if availability:
            queryset = queryset.filter(availability__iexact=availability)
        if freshness:
            queryset = queryset.filter(freshness__gt=parse_date(freshness))
            
        if is_Organic is not None:
            queryset = queryset.filter(is_Organic=(is_Organic.lower() == 'true'))
        
        return queryset
            