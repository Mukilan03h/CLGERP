from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Application, Admission
from .serializers import ApplicationSerializer, AdmissionSerializer, ApplicationTransitionSerializer
from workflow.models import Transition
from rest_framework.permissions import IsAuthenticated

class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'], url_path='transition')
    def transition(self, request, pk=None):
        application = self.get_object()
        serializer = ApplicationTransitionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        to_stage = serializer.validated_data['to_stage']
        user_role = request.user.role

        if not application.workflow or not application.current_stage:
            return Response({'error': 'Application is not assigned to a workflow.'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if a valid transition exists for the user's role
        valid_transition = Transition.objects.filter(
            workflow=application.workflow,
            from_stage=application.current_stage,
            to_stage=to_stage,
            role=user_role
        ).exists()

        if not valid_transition:
            return Response({'error': 'This transition is not allowed for your role.'}, status=status.HTTP_403_FORBIDDEN)

        # Perform the transition
        application.current_stage = to_stage
        application.save()

        return Response({'status': 'success', 'new_stage': to_stage.name}, status=status.HTTP_200_OK)

class AdmissionViewSet(viewsets.ModelViewSet):
    queryset = Admission.objects.all()
    serializer_class = AdmissionSerializer
    permission_classes = [IsAuthenticated]
