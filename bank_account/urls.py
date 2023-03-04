from django.urls import path

from .views import CreateAccountView, AccountDetailView, AccountListView, ChangeAccountActivation, ChangeAccountApproval

urlpatterns = [
    path('me/add-account/', CreateAccountView.as_view(), name='add-account'),
    path('list/', AccountListView.as_view(), name='account-list'),
    path('me/detail/', AccountDetailView.as_view(), name='account-detail'),
    path('me/change-activation/', ChangeAccountActivation.as_view(), name='change-activation'),
    path('me/change-approva/', ChangeAccountApproval.as_view(), name='change-approval'),
    path('account-type/add-account-type/', AccountDetailView.as_view(), name='add-account'),
]
