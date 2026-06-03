from django.urls import path, include
from rest_framework import routers
router = routers.DefaultRouter()

from .views import UserRegisterView

router.register(r"register",UserRegisterView)

urlpatterns = [
    path("", include(router.urls))
]


