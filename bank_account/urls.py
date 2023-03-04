from django.urls import path

from .views import CreateAccountView, AccountDetailView, AccountListView

urlpatterns = [
    path('me/add-account/', CreateAccountView.as_view(), name='add-account'),
    path('list/', AccountListView.as_view(), name='add-account'),
    path('me/detail/', AccountDetailView.as_view(), name='add-account'),
]
