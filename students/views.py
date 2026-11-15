from django.shortcuts import render
from .models import ClassNumber, Student
from .serializers import ClassNumberSerializer, StudentSerializer
from rest_framework import viewsets
from config.permissions import IsAdminOrReadOnly

# Create your views here.
class ClassNumberViewSet(viewsets.ModelViewSet):
    queryset = ClassNumber.objects.all().order_by("number")
    serializer_class = ClassNumberSerializer
    permission_classes = [IsAdminOrReadOnly]


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all().order_by('last_name')
    serializer_class = StudentSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        qys = Student.objects.all().order_by("last_name")
        if hasattr(user, "students") and not (user.is_staff or user.is_superuser):
            return qys.filter(user=user)
        return qys