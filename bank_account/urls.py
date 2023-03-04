from django.urls import path

from .views import CreateAccountView, AccountDetailView, AccountListView, ChangeAccountActivation, \
    ChangeAccountApproval, AccountTypeList, AccountTypeDetail

urlpatterns = [
    path('me/add-account/', CreateAccountView.as_view(), name='add_account'),
    path('list/', AccountListView.as_view(), name='account_list'),
    path('me/detail/', AccountDetailView.as_view(), name='account_detail'),
    path('me/change-activation/', ChangeAccountActivation.as_view(), name='change_activation'),
    path('me/change-approva/', ChangeAccountApproval.as_view(), name='change_approval'),
    path('account-type/add-account-type/', AccountDetailView.as_view(), name='add_account_type'),
    path('account-type/list/', AccountTypeList.as_view(), name='account_type_list'),
    path('account-type/detail/<int:pk>', AccountTypeDetail.as_view(), name='account_type_detail'),
]
