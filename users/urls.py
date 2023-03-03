from django.urls import path
from .views import RegisterView, LoginView, LogoutView, UserView, UserListView, ChangePasswordView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('user/', UserView.as_view(), name='user'),
    path('user/list/', UserListView.as_view(), name='user_list'),
    path('user/change-password/', ChangePasswordView.as_view(), name='change_password'),

]
