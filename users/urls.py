from .views import RegisterView, LoginView , LogoutView, ForgotPasswordView, PasswordResetView
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path("register", RegisterView.as_view()),
    path("login", LoginView.as_view()),
    path("logout", LogoutView.as_view()),
    path("token/refresh", TokenRefreshView.as_view()),
    path("password-forgot", ForgotPasswordView.as_view()),
    path("password-reset/<uidb64>/<token>", PasswordResetView().as_view())
    
]


