from django.shortcuts import render
from rest_framework import viewsets
from .models import Teacher
from .serializers import TeacherSerializer
from config.permissions import IsAdminOrReadOnly

# Create your views here.
class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all().order_by('last_name')
    serializer_class = TeacherSerializer
    permission_classes = [IsAdminOrReadOnly]