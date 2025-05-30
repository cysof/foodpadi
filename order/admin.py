from django.contrib import admin
from django.core.exceptions import ValidationError
from django.contrib import messages
from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'buyer', 'crop', 'quantity', 'status', 'total_price', 'ordered_at')
    list_filter = ('status', 'ordered_at')
    list_display_links = ('id', 'buyer')
    list_editable = ( 'status',)
    search_fields = ('buyer__username', 'crop__crop_name')
    readonly_fields = ('ordered_at', 'updated_at', 'total_price')

    fieldsets = (
        (None, {
            'fields': ('buyer', 'crop', 'quantity', 'status', 'delivery_address', 'notes')
        }),
        ('Audit Info', {
            'fields': ('price_per_unit', 'total_price', 'ordered_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    actions = ['cancel_selected_orders', 'mark_as_shipped', 'mark_as_delivered']

    def cancel_selected_orders(self, request, queryset):
        count = 0
        for order in queryset:
            if order.can_be_cancelled:
                order.cancel_order()
                count += 1
        self.message_user(request, f"{count} orders cancelled successfully.", level=messages.SUCCESS)
    cancel_selected_orders.short_description = "Cancel selected orders"

    def mark_as_shipped(self, request, queryset):
        count = 0
        for order in queryset:
            try:
                order.update_status(Order.OrderStatus.SHIPPED)
                count += 1
            except ValidationError as e:
                self.message_user(request, f"Order #{order.id} not updated: {e}", level=messages.WARNING)
        self.message_user(request, f"{count} orders marked as shipped.", level=messages.SUCCESS)
    mark_as_shipped.short_description = "Mark selected orders as shipped"

    def mark_as_delivered(self, request, queryset):
        count = 0
        for order in queryset:
            try:
                order.update_status(Order.OrderStatus.DELIVERED)
                count += 1
            except ValidationError as e:
                self.message_user(request, f"Order #{order.id} not updated: {e}", level=messages.WARNING)
        self.message_user(request, f"{count} orders marked as delivered.", level=messages.SUCCESS)
    mark_as_delivered.short_description = "Mark selected orders as delivered"

    def get_readonly_fields(self, request, obj=None):
        readonly = list(self.readonly_fields)
        if obj:
            readonly.append('price_per_unit')
        return readonly
