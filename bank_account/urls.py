from django.urls import path

from .views import CreateAccountView

urlpatterns = [
    path('add-account/', CreateAccountView.as_view(), name='add-account'),
]
