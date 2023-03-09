from django.contrib import admin
from bank.models import TransactionType, TransactionWay, TransactionDestinationUser, Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_filter = ['user', 'type', 'is_done', 'is_fail']
    list_display = ['user', 'type', 'created_at', 'is_done', 'is_fail']
    list_editable = ['is_done', 'is_fail']


@admin.register(TransactionType)
class TransactionTypeAdmin(admin.ModelAdmin):
    list_filter = ['is_active']
    list_display = ['title', 'is_active']
    list_editable = ['is_active']


@admin.register(TransactionWay)
class TransactionWayAdmin(admin.ModelAdmin):
    list_filter = ['is_active']
    list_display = ['title', 'is_active']
    list_editable = ['is_active']


@admin.register(TransactionDestinationUser)
class TransactionDestinationUserAdmin(admin.ModelAdmin):
    list_filter = ['is_active', 'is_valid']
    list_display = ['destination_name', 'card_number', 'is_active', 'is_valid']
    list_editable = ['is_active', 'is_valid']
