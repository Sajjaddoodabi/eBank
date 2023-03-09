from django.contrib import admin
from bank.models import TransactionType, TransactionWay, TransactionDestinationUser, Transaction


admin.site.register(Transaction)
admin.site.register(TransactionType)
admin.site.register(TransactionWay)
admin.site.register(TransactionDestinationUser)
