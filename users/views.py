from django.shortcuts import render

from .serializers import UserRegisterSerializer
from .models import User

from rest_framework import viewsets

class UserRegisterView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
