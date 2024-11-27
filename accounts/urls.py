from django.urls import path
from accounts.views import UserDetailView, UserListView


urlpatterns = [
    path('users/', UserListView.as_view(), name = 'users'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user_detail')
]

