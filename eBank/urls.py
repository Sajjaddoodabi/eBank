from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/account/', include('users.urls')),
    path('api/bank-account/', include('bank_account.urls')),
    path('api/bank/', include('bank.urls')),
]
