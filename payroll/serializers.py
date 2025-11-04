from rest_framework import serializers
from .models import Salary, Payslip, PayslipEntry

class SalarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Salary
        fields = '__all__'

class PayslipEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = PayslipEntry
        fields = '__all__'

class PayslipSerializer(serializers.ModelSerializer):
    entries = PayslipEntrySerializer(many=True, read_only=True)

    class Meta:
        model = Payslip
        fields = '__all__'
