from django.db import models
from django.core.exceptions import ValidationError

DELIVERY_STATUS = (
    ('PENDING', 'Pending'),
    ('ON_THE_WAY', 'On the way'),
    ('DELIVERED', 'Delivered'),
    ('CANCELLED', 'Cancelled'),
)

class Delivery(models.Model):
    transporter = models.ForeignKey(
        'accounts.FarmPadiUser', on_delete=models.CASCADE, related_name='deliveries'
    )
    order = models.OneToOneField(
        'order.Order', on_delete=models.CASCADE, related_name='delivery'
    )
    delivery_address = models.CharField(max_length=255)
    delivery_date = models.DateField()
    delivery_fee = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_status = models.CharField(
        max_length=20, choices=DELIVERY_STATUS, default='PENDING'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    VALID_DELIVERY_TRANSITIONS = {
        'PENDING': ['ON_THE_WAY', 'CANCELLED'],
        'ON_THE_WAY': ['DELIVERED', 'CANCELLED'],
        'DELIVERED': [],
        'CANCELLED': [],
    }

    class Meta:
        verbose_name = 'Delivery'
        verbose_name_plural = 'Deliveries'
        ordering = ['-created_at']

    def __str__(self):
        return f"Delivery #{self.id} - {self.transporter.username} - {self.order.crop.crop_name}"

    def update_delivery_status(self, new_status):
        if new_status not in self.VALID_DELIVERY_TRANSITIONS.get(self.delivery_status, []):
            raise ValidationError(f"Invalid transition from {self.delivery_status} to {new_status}")
        self.delivery_status = new_status
        self.save()
