from django.contrib import admin
from .models import FarmPadiUser, Profile

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fields = ('profile_type', 'profile_picture', 'date_of_birth',)
    readonly_fields = ('user',)

@admin.register(FarmPadiUser)
class FarmPadiUserAdmin(admin.ModelAdmin):
    list_display = (
        'username', 
        'email', 
        'first_name',
        'last_name',
        'account_type', 
        'is_active',
        'created_at'
    )
    list_editable = ('is_active',)
    search_fields = ('username', 'email', 'first_name', 'last_name', 'phone_number')
    list_filter = ('account_type', 'is_active', 'is_staff', 'created_at')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'last_login')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': (
            'first_name', 
            'last_name', 
            'email', 
            'gender', 
            'phone_number',
            'address',
            'account_type'
        )}),
        ('Permissions', {'fields': (
            'is_active',
            'is_staff',
            'is_superuser',
            'groups',
            'user_permissions'
        )}),
        ('Important dates', {'fields': ('last_login', 'created_at')}),
    )

    inlines = [ProfileInline]

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'profile_type')
    search_fields = ('user__username', 'user__email')
    list_filter = ('profile_type',)
    readonly_fields = ('user',)
    raw_id_fields = ('user',)
