from django.core.mail import send_mail
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Application, Admission
from .serializers import ApplicationSerializer, AdmissionSerializer, ApplicationTransitionSerializer
from workflow.models import Transition, Stage
from notifications.models import Notification
from auth_app.models import User
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

        # --- Notification Logic ---

        # 1. Notify applicant if the stage is final
        if to_stage.is_final:
            send_mail(
                subject=f'Update on your application to College ERP',
                message=f'Dear {application.first_name},\n\nYour application has been moved to the "{to_stage.name}" stage.\n\nThank you for applying.',
                from_email='noreply@collegeerp.com',
                recipient_list=[application.email],
                fail_silently=False, # Set to True in production
            )

        # 2. Notify staff for the next possible stages
        next_transitions = Transition.objects.filter(workflow=application.workflow, from_stage=to_stage)
        next_roles = {t.role for t in next_transitions}

        if next_roles:
            next_actors = User.objects.filter(role__in=next_roles)
            message = f"Application for {application.first_name} {application.last_name} has been moved to '{to_stage.name}' and requires action."
            for actor in next_actors:
                Notification.objects.create(recipient=actor, message=message)

        return Response({'status': 'success', 'new_stage': to_stage.name}, status=status.HTTP_200_OK)

class AdmissionViewSet(viewsets.ModelViewSet):
    queryset = Admission.objects.all()
    serializer_class = AdmissionSerializer
    permission_classes = [IsAuthenticated]
