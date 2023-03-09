from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'mobile', 'is_active', 'is_approved', 'is_staff']
    list_editable = ['is_active', 'is_approved']
    list_filter = ['is_active', 'is_approved', 'is_staff', 'is_superuser']
