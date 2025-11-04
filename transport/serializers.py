from rest_framework import serializers
from .models import Vehicle, Route, TransportAllocation

class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = '__all__'

class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = '__all__'

class TransportAllocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransportAllocation
        fields = '__all__'
