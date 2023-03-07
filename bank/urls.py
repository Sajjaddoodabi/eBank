from django.urls import path
from .views import CreateTransactionDestinationView, TransactionDestinationListAll, TransactionDestinationAllList, \
    ChangeTransactionDestinationActivation, ChangeTransactionDestinationValidation, TransactionDestinationDetailView, \
    CreateTransactionTypeView, TransactionTypeListAllView, TransactionTypeListActiveView, TransactionTypeDetailView, \
    ChangeTransactionTypeActivationView, CreateTransactionWayView, TransactionWayDetailView, TransactionWayAllListView, \
    TransactionWayActiveListView, ChangeTransactionWayActivationView, TransactionDestinationActiveList

urlpatterns = [
    path('me/destination/create-destination/', CreateTransactionDestinationView.as_view(), name='create_destination'),
    path('me/destination/list/', TransactionDestinationAllList.as_view(), name='my_destination_list'),
    path('me/destination/detail/<int:pk>/', TransactionDestinationDetailView.as_view(), name='destination_detail'),
    path('destination/list/all/', TransactionDestinationListAll.as_view(), name='destination_list_all'),
    path('destination/list/active/', TransactionDestinationActiveList.as_view(), name='destination_list_active'),
    path('destination/change-activation/<int:pk>/', ChangeTransactionDestinationActivation.as_view(), name='change_activation_destination'),
    path('destination/change-validation/<int:pk>/', ChangeTransactionDestinationValidation.as_view(), name='change_validation_destination'),
    path('type/add-type/', CreateTransactionTypeView.as_view(), name='add_type'),
    path('type/list/all/', TransactionTypeListAllView.as_view(), name='type_list_all'),
    path('type/list/active/', TransactionTypeListActiveView.as_view(), name='type_list_active'),
    path('type/detail/<int:pk>/', TransactionTypeDetailView.as_view(), name='type_detail'),
    path('type/detail/change-activation/<int:pk>/', ChangeTransactionTypeActivationView.as_view(), name='type_activation'),
    path('way/add-way/', CreateTransactionWayView.as_view(), name='add_transaction_way'),
    path('way/list/all/', TransactionWayAllListView.as_view(), name='transaction_way_list_all'),
    path('way/list/active/', TransactionWayActiveListView.as_view(), name='transaction_way_list_active'),
    path('way/detail/<int:pk>/', TransactionWayDetailView.as_view(), name='transaction_way_detail'),
    path('way/detail/change-activation/<int:pk>/', ChangeTransactionWayActivationView.as_view(), name='transaction_way_activation'),
]
