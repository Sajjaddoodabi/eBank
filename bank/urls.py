from django.urls import path
from .views import CreateTransactionDestinationView, TransactionDestinationListAll, TransactionDestinationList, \
    ChangeTransactionDestinationActivation, ChangeTransactionDestinationValidation, TransactionDestinationDetailView, \
    CreateTransactionTypeView, TransactionTypeListView, TransactionTypeDetailView, ChangeTransactionTypeActivation, \
    CreateTransactionWayView, TransactionWayDetailView

urlpatterns = [
    path('me/destination/create-destination/', CreateTransactionDestinationView.as_view(), name='create_destination'),
    path('me/destination/list/', TransactionDestinationList.as_view(), name='my_destination_list'),
    path('me/destination/detail/<int:pk>/', TransactionDestinationDetailView.as_view(), name='destination_detail'),
    path('destination/list/', TransactionDestinationListAll.as_view(), name='destination_list'),
    path('destination/change-activation/<int:pk>/', ChangeTransactionDestinationActivation.as_view(), name='change_activation_destination'),
    path('destination/change-validation/<int:pk>/', ChangeTransactionDestinationValidation.as_view(), name='change_validation_destination'),
    path('type/add-type/', CreateTransactionTypeView.as_view(), name='add_type'),
    path('type/list/', TransactionTypeListView.as_view(), name='type_list'),
    path('type/detail/<int:pk>/', TransactionTypeDetailView.as_view(), name='type_detail'),
    path('type/detail/change-activation/<int:pk>/', ChangeTransactionTypeActivation.as_view(), name='type_activation'),
    path('way/add-way/', CreateTransactionWayView.as_view(), name='add_transaction_way'),
    path('way/detail/<int:pk>/', TransactionWayDetailView.as_view(), name='transaction_way_detail'),
]
