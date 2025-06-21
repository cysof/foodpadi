from rest_framework import permissions

class CropListingPermission(permissions.BasePermission):
    """
    Allow anyone to read (GET, HEAD, OPTIONS).
    Only authenticated users with account_type='FARMER' can create or edit.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        return (
            request.user
            and request.user.is_authenticated
            and getattr(request.user, 'account_type', '').upper() == 'FARMER'
        )

    def has_object_permission(self, request, view, obj):
        # Anyone can view; only owners can update/delete
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.farmer == request.user
