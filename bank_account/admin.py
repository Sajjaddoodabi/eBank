from django.contrib import admin
from .models import Card, AccountType, Account


class CardInline(admin.TabularInline):
    model = Card


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    inlines = [
        CardInline
    ]
    list_display = ['user', 'type', 'balance', 'is_active', 'is_approved']
    list_editable = ['is_active', 'is_approved']
    list_filter = ['is_active', 'is_approved']


@admin.register(AccountType)
class AccountTypeAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active']
    list_editable = ['is_active']
    list_filter = ['is_active']


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ['account', 'card_number', 'cvv2', 'created_date', 'expire_date', 'is_active', 'is_ban']
    list_editable = ['is_active', 'is_ban']
    list_filter = ['is_active', 'is_ban']
