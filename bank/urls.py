from django.urls import path
from .views import CreateTransactionDestinationView

urlpatterns = [
    path('me/destination/create-destination/', CreateTransactionDestinationView.as_view(), name='create_destination'),
]
