from django.shortcuts import render
from .serializers import SubjectSerializer
from .models import Subject
from rest_framework import viewsets
from config.permissions import IsAdminOrReadOnly

# Create your views here.
class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all().order_by('grade')
    serializer_class = SubjectSerializer
    permission_classes = [IsAdminOrReadOnly]