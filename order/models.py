from decimal import Decimal
from django.db import models
from django.core.exceptions import ValidationError
from accounts.models import FarmPadiUser
from croplisting.models import CropListing


class Order(models.Model):
    class OrderStatus(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        CONFIRMED = 'CONFIRMED', 'Confirmed'
        SHIPPED = 'SHIPPED', 'Shipped'
        DELIVERED = 'DELIVERED', 'Delivered'
        CANCELLED = 'CANCELLED', 'Cancelled'

    VALID_TRANSITIONS = {
        OrderStatus.PENDING: [OrderStatus.CONFIRMED, OrderStatus.CANCELLED],
        OrderStatus.CONFIRMED: [OrderStatus.SHIPPED, OrderStatus.CANCELLED],
        OrderStatus.SHIPPED: [OrderStatus.DELIVERED],
        OrderStatus.DELIVERED: [],
        OrderStatus.CANCELLED: [],
    }

    buyer = models.ForeignKey(FarmPadiUser, on_delete=models.CASCADE, related_name='orders')
    crop = models.ForeignKey(CropListing, on_delete=models.CASCADE, related_name='orders')
    quantity = models.PositiveIntegerField(default=1)

    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, editable=False)

    status = models.CharField(max_length=20, choices=OrderStatus.choices, default=OrderStatus.PENDING)
    ordered_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    delivery_address = models.CharField(max_length=255)
    notes = models.TextField(blank=True, null=True, help_text="Special instructions or notes")

    class Meta:
        ordering = ['-ordered_at']
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    def __str__(self):
        return f"Order #{self.id} - {self.buyer.username} - {self.crop.crop_name}"

    def clean(self):
        if self.quantity > self.crop.quantity:
            raise ValidationError(
                f"Requested quantity ({self.quantity}) exceeds available stock ({self.crop.quantity})"
            )
        if self.buyer == self.crop.farmer:
            raise ValidationError("You cannot order your own crop listing")

    def save(self, *args, **kwargs):
        self.full_clean()  # Enforce model-level validation before saving
        if not self.price_per_unit:
            self.price_per_unit = self.crop.price_per_unit
        self.total_price = Decimal(self.quantity) * self.price_per_unit
        super().save(*args, **kwargs)

    def update_status(self, new_status):
        if new_status not in self.VALID_TRANSITIONS.get(self.status, []):
            raise ValidationError(f"Cannot change status from {self.status} to {new_status}")
        self.status = new_status
        self.save()

    def cancel_order(self):
        if self.can_be_cancelled:
            self.status = self.OrderStatus.CANCELLED
            self.save()
            return True
        return False

    def confirm_order(self):
        if self.status == self.OrderStatus.PENDING:
            self.status = self.OrderStatus.CONFIRMED
            self.save()
            return True
        return False

    @property
    def can_be_cancelled(self):
        return self.status in {
            self.OrderStatus.PENDING,
            self.OrderStatus.CONFIRMED,
        }

    @property
    def is_completed(self):
        return self.status == self.OrderStatus.DELIVERED