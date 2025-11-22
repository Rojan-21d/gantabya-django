from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    # Fields shown in the admin panel
    list_display = ('email', 'username', 'user_type', 'vehicle_type', 'vehicle_capacity_kg', 'is_staff', 'is_active')
    list_filter = ('user_type', 'is_staff', 'is_active')

    # Email becomes the main login field
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('username', 'contact', 'address', 'profile_pic')}),
        ('Carrier Vehicle', {'fields': ('vehicle_type', 'vehicle_capacity_kg', 'base_rate_per_km', 'current_latitude', 'current_longitude')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'user_type', 'is_staff', 'is_active')
        }),
    )

    search_fields = ('email', 'username')
    ordering = ('email',)


admin.site.register(CustomUser, CustomUserAdmin)
