from django.contrib import admin
from .models import CropListing



class CropListingAdmin(admin.ModelAdmin):
    # Define the fields to display in the admin interface
    list_display = ('farmer', 'crop_name', 'quantity', 'price_per_unit', 'created_at')
    list_filter = ('farmer', 'created_at')
    search_fields = ('farmer__username', 'crop_name')
    readonly_fields = ('created_at',)

    # Define the fields to display in the detail view
    fieldsets = (
        (None, {'fields': ('farmer', 'crop_name', 'crop_description', 'quantity', 'unit', 'location', 'price_per_unit', 'harvested_date', 'is_Organic', 'availability', 'img')}),
        ('Audit', {'fields': ('created_at',), 'classes': ('collapse',)}),
    )

    # Define the actions to perform on the model instances
    actions = ['approve_crop_listing', 'reject_crop_listing']

    def approve_crop_listing(self, request, queryset):
        # Implement the logic to approve a crop listing
        pass

    def reject_crop_listing(self, request, queryset):
        # Implement the logic to reject a crop listing
        pass

    approve_crop_listing.short_description = 'Approve selected crop listings'
    reject_crop_listing.short_description = 'Reject selected crop listings'

admin.site.register(CropListing, CropListingAdmin)
    
    