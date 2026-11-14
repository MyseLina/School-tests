from django.urls import path, include
from .views import AttemptViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'attempt', AttemptViewSet)

urlpatterns = [
    path('', include(router.urls)),
]