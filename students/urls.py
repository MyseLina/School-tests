from django.urls import include, path
from .views import ClassNumberViewSet, StudentViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'classes', ClassNumberViewSet)
router.register(r'students', StudentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]