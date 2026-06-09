from django.shortcuts import render

from .serializers import UserRegisterSerializer, LoginSerializer
from django.contrib.auth import get_user_model

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


User = get_user_model()

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
             
class ForgotPasswordView(APIView):

    def post(self, request):

        email = request.data.get("email", "").strip().lower()

        user = User.objects.filter(email__iexact=email).first()

        if not user:
            return Response(
                {"message": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        uidb64 = urlsafe_base64_encode(force_bytes(user.id))
        token = PasswordResetTokenGenerator().make_token(user)

        reset_link = f"http://127.0.0.1:8000/auth/password-reset/{uidb64}/{token}"
       

        send_mail(
            subject="Account Password Reset",
            message=f"Reset your password: {reset_link}",
            from_email="noreply@example.com",
            recipient_list=[email]
        )

        return Response({
            "message": "Reset link sent successfully"
        })           
           

            
       
            
            
      


class PasswordResetView(APIView):
    
    def post(self, request, uidb64, token):
        
        
        try:
            
           uid  = force_str(urlsafe_base64_decode(uidb64))
           user = User.objects.get(id=uid)
                             
                             
                             
        except Exception:
            return Response({
                
                "message":"Invalid link"
                
            }) 
            
            
        if not PasswordResetTokenGenerator().check_token(user,token):
             return Response({
                "error": "Invalid or expired token"
            }, status=400)
          
        password = request.data.get("password")
        user.set_password(password)
        user.save()
        
        return Response({
            "message":"Password reseted successfully"
        })                             
    
  
