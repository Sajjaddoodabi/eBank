from django.contrib import admin
from .models import Card, AccountType, Account


class CardInline(admin.TabularInline):
    model = Card


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    inlines = [
        CardInline
    ]


admin.site.register(AccountType)
admin.site.register(Card)
