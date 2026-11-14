from .models import ClassNumber, Student
from rest_framework import serializers

class ClassNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassNumber
        fields = '__all__'


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'