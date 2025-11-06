from rest_framework import serializers
from .models import Application, Admission
from workflow.models import Stage

class ApplicationTransitionSerializer(serializers.Serializer):
    to_stage = serializers.PrimaryKeyRelatedField(queryset=Stage.objects.all())

class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = '__all__'

class AdmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admission
        fields = '__all__'
