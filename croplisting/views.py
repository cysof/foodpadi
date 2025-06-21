from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import CropListing
from .serializers import CropListingSerializer
from .permissions import CropListingPermission
from django.utils.dateparse import parse_date
from rest_framework.exceptions import PermissionDenied

class CropListingViewSet(viewsets.ModelViewSet):
    serializer_class = CropListingSerializer
    queryset = CropListing.objects.all().order_by('-created_at')
    permission_classes = [CropListingPermission]  # Your custom permission handles everything
    
    def get_permissions(self):
        """
        Use custom permission for most actions, but require authentication for my_listings
        """
        if self.action == 'my_listings':
            # Farmer dashboard requires authentication
            return [IsAuthenticated()]
        return [CropListingPermission()]

    def perform_create(self, serializer):
        user = self.request.user
        if not user.is_authenticated:
            raise PermissionDenied("Authentication required.")
        if user.account_type != 'FARMER':
            raise PermissionDenied("Only farmers can create crop listings.")
        serializer.save(farmer=user)

    def get_queryset(self):
        """
        Returns queryset based on the action:
        - For 'my_listings' action: returns only current farmer's listings
        - For other actions: returns all listings with optional filtering
        """
        # Check if this is the farmer's dashboard view (my_listings action)
        if self.action == 'my_listings':
            if not self.request.user.is_authenticated:
                raise PermissionDenied("Authentication required.")
            if self.request.user.account_type != 'FARMER':
                raise PermissionDenied("Only farmers can view their listings.")
            return CropListing.objects.filter(farmer=self.request.user).order_by('-created_at')
        
        # For general listing view, apply filters
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

    @action(detail=False, methods=['get'], url_path='my-listings')
    def my_listings(self, request):
        """
        Custom endpoint for farmers to view their own crop listings
        URL: /api/crops/my-listings/
        """
        if not request.user.is_authenticated:
            raise PermissionDenied("Authentication required.")
        if request.user.account_type != 'FARMER':
            raise PermissionDenied("Only farmers can view their listings.")
        
        # Get farmer's listings with optional filtering
        queryset = CropListing.objects.filter(farmer=request.user).order_by('-created_at')
        
        # Apply same filtering logic as general queryset
        params = request.query_params
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
        
        # Paginate results
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)