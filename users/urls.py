from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import LoginView, CreateUserView, UserListView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('users/create/', CreateUserView.as_view(), name='user-create'),
]