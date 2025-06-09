from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticated
from .models import CropListing
from .serializers import CropListingSerializer
from rest_framework.exceptions import PermissionDenied

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
    queryset = CropListing.objects.all().order_by('-created_at')
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