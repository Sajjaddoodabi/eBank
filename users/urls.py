from django.urls import path
from .views import RegisterView, LoginView, LogoutView, UserView, UserListAllView, UserListApprovedView, \
    UserListActiveView, ChangePasswordView, ResetPasswordView, \
    UserUpdateView, UserDeleteView, ChangeUserApprovalView, ChangeUserActivationView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('user/', UserView.as_view(), name='user'),
    path('user/detail/update/', UserUpdateView.as_view(), name='user'),
    path('user/detail/delete/', UserDeleteView.as_view(), name='user'),
    path('user/list/all/', UserListAllView.as_view(), name='user_list_all'),
    path('user/list/approve/', UserListApprovedView.as_view(), name='user_list_approve'),
    path('user/list/active/', UserListActiveView.as_view(), name='user_list_active'),
    path('user/change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('user/reset-password/', ResetPasswordView.as_view(), name='reset_password'),
    path('user/change-approval/<int:pk>/', ChangeUserApprovalView.as_view(), name='user_change_activation'),
    path('user/change-activation/<int:pk>/', ChangeUserActivationView.as_view(), name='user_change_approval'),

]
