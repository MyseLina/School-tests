from django.shortcuts import render
from .models import Attempt
from .serializers import AttemptSerializer
from rest_framework import viewsets
from config.permissions import is_admin

# Create your views here.
class AttemptViewSet(viewsets.ModelViewSet):
    queryset = Attempt.objects.all()
    serializer_class = AttemptSerializer
    http_method_names = ["get", "head", "options"]

    def get_queryset(self):
        qys = Attempt.objects.all().order_by("-started")
        user = self.request.user
        if is_admin(user):
            return qys
        if hasattr(user, "teacher"):
            return qys.filter(test__teacher=user.teacher)
        if hasattr(user, "student"):
            return qys.filter(student=user.student)
        return qys.none()