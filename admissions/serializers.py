from rest_framework import serializers
from .models import ApplicationForm, MeritList

class ApplicationFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationForm
        fields = '__all__'

class MeritListSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeritList
        fields = '__all__'
