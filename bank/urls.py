from django.urls import path
from .views import CreateTransactionDestinationView, TransactionDestinationListAll, TransactionDestinationList, \
    ChangeTransactionDestinationActivation, ChangeTransactionDestinationValidation, TransactionDestinationDetailView, \
    CreateTransactionTypeView, TransactionTypeListView, TransactionDetailView

urlpatterns = [
    path('me/destination/create-destination/', CreateTransactionDestinationView.as_view(), name='create_destination'),
    path('me/destination/list/', TransactionDestinationList.as_view(), name='my_destination_list'),
    path('me/destination/detail/<int:pk>', TransactionDestinationDetailView.as_view(), name='destination_detail'),
    path('destination/list/', TransactionDestinationListAll.as_view(), name='destination_list'),
    path('destination/change-activation/', ChangeTransactionDestinationValidation.as_view(), name='change_activation_destination'),
    path('destination/change-validatoin/', ChangeTransactionDestinationActivation.as_view(), name='change_validation_destination'),
    path('type/add-type/', CreateTransactionTypeView.as_view(), name='add_type'),
    path('type/list/', TransactionTypeListView.as_view(), name='type_list'),
    path('type/detail/<int:pk>', TransactionDetailView.as_view(), name='type_detail'),
]
