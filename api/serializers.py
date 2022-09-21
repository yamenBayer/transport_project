from dataclasses import field
from rest_framework.serializers import ModelSerializer
from .models import Trip

class TripSerializer(ModelSerializer):
    class Meta:
        model = Trip
        fields = '__all__'