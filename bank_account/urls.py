from django.urls import path

from .views import CreateAccountView, AccountDetailView, AccountListAllView, AccountListApproveView, \
    AccountListActiveView, ChangeAccountActivation, \
    ChangeAccountApproval, AccountTypeListAllView, AccountTypeListActiveView, AccountTypeDetailView, \
    ChangeAccountTypeActivationView, CreateAccountTypeView, \
    CreateCardView, ChangeCardActivationView, ChangeCardBanStatusView, CardRenewalView, CardListAllView, CardListActiveView, \
    CardListBanView, CardDetailView, MyAccountDetail

urlpatterns = [
    path('me/add-account/', CreateAccountView.as_view(), name='add_account'),
    path('account/list/all/', AccountListAllView.as_view(), name='account_list_all'),
    path('account/list/active/', AccountListActiveView.as_view(), name='account_list_active'),
    path('account/list/approve/', AccountListApproveView.as_view(), name='account_list_approve'),
    path('account/detail/<int:pk>/', AccountDetailView.as_view(), name='account_detail'),
    path('me/account/detail/', MyAccountDetail.as_view(), name='my_account_detail'),
    path('me/change-activation/', ChangeAccountActivation.as_view(), name='change_activation'),
    path('me/change-approval/', ChangeAccountApproval.as_view(), name='change_approval'),
    path('me/card/add-card/', CreateCardView.as_view(), name='add_card'),
    path('me/card/detail/<int:pk>/', CardDetailView.as_view(), name='add_card'),
    path('card/list/all/', CardListAllView.as_view(), name='card_list_all'),
    path('card/list/ban/', CardListBanView.as_view(), name='card_list_ban'),
    path('card/list/active/', CardListActiveView.as_view(), name='card_list_active'),
    path('me/card/card-renewal/', CardRenewalView.as_view(), name='card_renewal'),
    path('me/card/change-activation/', ChangeCardActivationView.as_view(), name='change_card_activation'),
    path('me/card/change-ban-status/', ChangeCardBanStatusView.as_view(), name='change_card_ban_status'),
    path('account-type/add-account-type/', CreateAccountTypeView.as_view(), name='add_account_type'),
    path('account-type/list/all/', AccountTypeListAllView.as_view(), name='account_type_list_all'),
    path('account-type/list/active/', AccountTypeListActiveView.as_view(), name='account_type_list_active'),
    path('account-type/detail/<int:pk>/', AccountTypeDetailView.as_view(), name='account_type_detail'),
    path('account-type/detail/change-activation/<int:pk>/', ChangeAccountTypeActivationView.as_view(), name='account_type_activation'),
]
