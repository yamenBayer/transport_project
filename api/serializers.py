from dataclasses import field
from rest_framework.serializers import ModelSerializer
from .models import Profile, Trip, Reservation

class TripSerializer(ModelSerializer):
    class Meta:
        model = Trip
        fields = '__all__'

class ProfileSerializer(ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

class ReservationSerializer(ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'