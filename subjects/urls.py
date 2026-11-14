from django.urls import include, path
from .views import SubjectViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register('subject', SubjectViewSet)

urlpatterns = [
    path('', include(router.urls))
]