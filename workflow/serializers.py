from rest_framework import serializers
from .models import Workflow, Stage, Transition

class WorkflowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workflow
        fields = '__all__'

class StageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stage
        fields = '__all__'

class TransitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transition
        fields = '__all__'
