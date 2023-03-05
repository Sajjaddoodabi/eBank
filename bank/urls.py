from django.urls import path
from .views import CreateTransactionDestinationView, TransactionDestinationListAll, TransactionDestinationList, \
    ChangeTransactionDestinationActivation, ChangeTransactionDestinationValidation, TransactionDestinationDetailView

urlpatterns = [
    path('me/destination/create-destination/', CreateTransactionDestinationView.as_view(), name='create_destination'),
    path('me/destination/list/', TransactionDestinationList.as_view(), name='my_destination_list'),
    path('me/destination/detail/<int:pk>', TransactionDestinationDetailView.as_view(), name='destination_detail'),
    path('/destination/list/', TransactionDestinationListAll.as_view(), name='destination_list'),
    path('/destination/change-activation/', ChangeTransactionDestinationValidation.as_view(), name='change_activation_destination'),
    path('/destination/change-validatoin/', ChangeTransactionDestinationActivation.as_view(), name='change_validation_destination'),
]
