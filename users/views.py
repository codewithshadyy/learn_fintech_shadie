from django.shortcuts import render

from .serializers import UserRegisterSerializer, LoginSerializer
from .models import User
from rest_framework.response import Response

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail

class RegisterView(APIView):
    
    class Meta:
        queryset = User.objects.all()
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            
            return Response({
                "message":"User registered successfully"
                
            }, status=status.HTTP_201_CREATED)
            
        return Response(serializer.errors,status=400) 
    
    
class LoginView(APIView):
    permission_classes = [AllowAny]
   
            
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        refresh = RefreshToken.for_user(user)
        
        
        return Response({
            
            "data":{
                "id":user.id,
                "username":user.username,
                "email":user.email,
                "message":f"welcome back {user.username}"
            },
       
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }, status=status.HTTP_200_OK)       
            
        
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
       
       try:
           
           refresh_token = request.data["refresh"]
           token = RefreshToken(refresh_token)
           
           token.blacklist()
           
           return Response({
               "message":"Logged out successfully"
           })
           
       except Exception:
           return Response({
               "message":"Invalid token"
           }, status=status.HTTP_400_BAD_REQUEST)   
           
           
           
    
  
