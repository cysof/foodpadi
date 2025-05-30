from django.contrib import admin
from .models import Delivery
from accounts.models import FarmPadiUser

@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'transporter',
        'order',
        'delivery_status',
        'delivery_date',
        'delivery_fee',
        'delivery_address',
    )
    list_filter = ('delivery_status', 'delivery_date', 'transporter')
    search_fields = (
        'transporter__username',
        'order__buyer__username',
        'order__crop__crop_name',
        'delivery_address',
    )
    readonly_fields = ('created_at', 'updated_at', 'delivery_address')

    fieldsets = (
        (None, {
            'fields': (
                'transporter',
                'order',
                'delivery_address',
                'delivery_date',
                'delivery_fee',
                'delivery_status',
            )
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'transporter':
            kwargs["queryset"] = FarmPadiUser.objects.filter(account_type='TRANSPORTER')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    def save_model(self, request, obj, form, change):
        # On save, always set delivery_address from the related order
        if obj.order:
            obj.delivery_address = obj.order.delivery_address
        super().save_model(request, obj, form, change)