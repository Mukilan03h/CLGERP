from rest_framework import generics
from .models import FeeStructure, PaymentRecord
from .serializers import FeeStructureSerializer, PaymentRecordSerializer
from auth_app.middleware import StandardizedResponseMiddleware

class FeeStructureListCreateView(generics.ListCreateAPIView):
    queryset = FeeStructure.objects.all()
    serializer_class = FeeStructureSerializer
    renderer_classes = [StandardizedResponseMiddleware]

class FeeStructureRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = FeeStructure.objects.all()
    serializer_class = FeeStructureSerializer
    renderer_classes = [StandardizedResponseMiddleware]

class PaymentRecordListCreateView(generics.ListCreateAPIView):
    queryset = PaymentRecord.objects.all()
    serializer_class = PaymentRecordSerializer
    renderer_classes = [StandardizedResponseMiddleware]

class PaymentRecordRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PaymentRecord.objects.all()
    serializer_class = PaymentRecordSerializer
    renderer_classes = [StandardizedResponseMiddleware]

class StudentFeeView(generics.ListAPIView):
    serializer_class = PaymentRecordSerializer
    renderer_classes = [StandardizedResponseMiddleware]

    def get_queryset(self):
        return PaymentRecord.objects.filter(student_id=self.kwargs['student_id'])
