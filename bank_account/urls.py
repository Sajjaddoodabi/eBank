from django.urls import path

from .views import CreateAccountView, AccountDetailView, AccountListView, ChangeAccountActivation, \
    ChangeAccountApproval, AccountTypeList, AccountTypeDetail, ChangeAccountTypeActivation, CreateAccountTypeView, \
    CreateCardView, ChangeCardActivation, ChangeCardBanStatus, CardRenewalView

urlpatterns = [
    path('me/add-account/', CreateAccountView.as_view(), name='add_account'),
    path('list/', AccountListView.as_view(), name='account_list'),
    path('me/detail/', AccountDetailView.as_view(), name='account_detail'),
    path('me/change-activation/', ChangeAccountActivation.as_view(), name='change_activation'),
    path('me/change-approva/', ChangeAccountApproval.as_view(), name='change_approval'),
    path('me/card/add-card/', CreateCardView.as_view(), name='add_card'),
    path('me/card/card-renewal/', CardRenewalView.as_view(), name='card_renewal'),
    path('me/card/change-activation/', ChangeCardActivation.as_view(), name='change_card_activation'),
    path('me/card/change-ban-status/', ChangeCardBanStatus.as_view(), name='change_card_ban_status'),
    path('account-type/add-account-type/', CreateAccountTypeView.as_view(), name='add_account_type'),
    path('account-type/list/', AccountTypeList.as_view(), name='account_type_list'),
    path('account-type/detail/<int:pk>', AccountTypeDetail.as_view(), name='account_type_detail'),
    path('account-type/detail/change-activation/<int:pk>', ChangeAccountTypeActivation.as_view(), name='account_type_activation'),
]
