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
        if hasattr(user, "teachers"):
            return qys.filter(test__teacher=user.teachers)
        if hasattr(user, "students"):
            return qys.filter(student=user.students)
        return qys.none()