from rest_framework import generics
from rest_framework.response import Response
from .models import ApplicationForm, MeritList
from .serializers import ApplicationFormSerializer, MeritListSerializer
from auth_app.middleware import StandardizedResponseMiddleware

class ApplicationFormListCreateView(generics.ListCreateAPIView):
    queryset = ApplicationForm.objects.all()
    serializer_class = ApplicationFormSerializer
    renderer_classes = [StandardizedResponseMiddleware]

class ApplicationFormRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ApplicationForm.objects.all()
    serializer_class = ApplicationFormSerializer
    renderer_classes = [StandardizedResponseMiddleware]

class ApplicationStatusView(generics.RetrieveAPIView):
    queryset = ApplicationForm.objects.all()
    serializer_class = ApplicationFormSerializer
    renderer_classes = [StandardizedResponseMiddleware]

class VerifyApplicationView(generics.UpdateAPIView):
    queryset = ApplicationForm.objects.all()
    serializer_class = ApplicationFormSerializer
    renderer_classes = [StandardizedResponseMiddleware]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.status = 'Verified'
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class MeritListListCreateView(generics.ListCreateAPIView):
    queryset = MeritList.objects.all()
    serializer_class = MeritListSerializer
    renderer_classes = [StandardizedResponseMiddleware]

class MeritListRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MeritList.objects.all()
    serializer_class = MeritListSerializer
    renderer_classes = [StandardizedResponseMiddleware]
