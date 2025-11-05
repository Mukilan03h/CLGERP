from rest_framework import serializers
from .models import Faculty, LeaveRequest
from attendance.models import Subject

class FacultySerializer(serializers.ModelSerializer):
    subjects = serializers.PrimaryKeyRelatedField(many=True, queryset=Subject.objects.all(), required=False)

    class Meta:
        model = Faculty
        fields = '__all__'

class LeaveRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveRequest
        fields = '__all__'
