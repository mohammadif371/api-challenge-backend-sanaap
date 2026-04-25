from django.urls import path
from .views import LoginView, CreateUserView, UserListView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/create/', CreateUserView.as_view(), name='user-create'),
]