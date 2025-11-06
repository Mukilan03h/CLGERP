from rest_framework import viewsets
from .models import Workflow, Stage, Transition
from .serializers import WorkflowSerializer, StageSerializer, TransitionSerializer
from .permissions import IsAdminUser

class WorkflowViewSet(viewsets.ModelViewSet):
    queryset = Workflow.objects.all()
    serializer_class = WorkflowSerializer
    permission_classes = [IsAdminUser]

class StageViewSet(viewsets.ModelViewSet):
    queryset = Stage.objects.all()
    serializer_class = StageSerializer
    permission_classes = [IsAdminUser]

class TransitionViewSet(viewsets.ModelViewSet):
    queryset = Transition.objects.all()
    serializer_class = TransitionSerializer
    permission_classes = [IsAdminUser]
