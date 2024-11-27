from django.shortcuts import render
from accounts.serializers import UserSerializer
from rest_framework import generics
from rest_framework.permissions import IsAdminUser 
from django.contrib.auth import get_user_model


class UserListView(generics.ListCreateAPIView):
    permission_classes = (IsAdminUser,)
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    
class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAdminUser,)
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
   