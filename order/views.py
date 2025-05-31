from rest_framework import viewsets, permissions
from .models import Order
from .serializers import OrderSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().order_by('-ordered_at')
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # Return only orders that belong to the authenticated user (as buyer)
        return self.queryset.filter(buyer=user)

    def perform_create(self, serializer):
        serializer.save(buyer=self.request.user)
