from django.urls import path, include
from rest_framework import routers
router = routers.DefaultRouter()

from .views import RegisterView

router.register(r"register",RegisterView)

urlpatterns = [
    path("", include(router.urls))
]


