# users/admin.py
from django.contrib import admin
from .models import UserProfile, OTPToken

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_display_name', 'phone_number', 'is_phone_verified', 'created_at')
    search_fields = ('user__username', 'phone_number', 'first_name', 'last_name')
    list_filter = ('is_phone_verified',)
    readonly_fields = ('created_at', 'updated_at') # Буларды өзгөртүүгө болбойт

    fieldsets = (
        (None, {'fields': ('user', 'phone_number', 'is_phone_verified')}),
        ('Жеке маалыматтар', {'fields': ('first_name', 'last_name', 'bio', 'date_of_birth')}),
        ('Профиль сүрөтү', {'fields': ('profile_picture',)}),
        ('Даталар', {'fields': ('created_at', 'updated_at')}),
    )

    def get_display_name(self, obj):
        return obj.get_full_name
    get_display_name.short_description = 'Толук аты'

class OTPTokenAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'otp_code', 'created_at', 'expires_at', 'is_used')
    list_filter = ('is_used', 'created_at')
    search_fields = ('phone_number', 'otp_code')
    readonly_fields = ('created_at', 'expires_at')

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(OTPToken, OTPTokenAdmin)