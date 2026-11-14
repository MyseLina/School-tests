from .models import Attempt
from rest_framework import serializers

class AttemptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attempt
        exclude = ["answers"]
        read_only_fields = ["student", "test", "score", "finished", "started"]