from django.contrib import admin
from .models import User, PhoneOTP


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("phone", "name", "is_staff", "is_active", "date_joined")
    search_fields = ("phone", "name")


@admin.register(PhoneOTP)
class PhoneOTPAdmin(admin.ModelAdmin):
    list_display = ("phone", "code", "created_at", "is_used")