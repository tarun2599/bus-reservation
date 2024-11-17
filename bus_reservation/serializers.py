from rest_framework import serializers
from .models import Bus, Reservation

class BusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bus
        fields = '__all__'

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'

class SearchBusSerializer(serializers.Serializer):
    source = serializers.CharField()
    destination = serializers.CharField()
    date = serializers.DateField()
