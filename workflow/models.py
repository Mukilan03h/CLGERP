from django.db import models
from auth_app.models import User

class Workflow(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Stage(models.Model):
    workflow = models.ForeignKey(Workflow, related_name='stages', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    order = models.IntegerField()

    class Meta:
        ordering = ['order']
        unique_together = ('workflow', 'name')

    def __str__(self):
        return f"{self.workflow.name} - {self.name}"

class Transition(models.Model):
    workflow = models.ForeignKey(Workflow, related_name='transitions', on_delete=models.CASCADE)
    from_stage = models.ForeignKey(Stage, related_name='from_transitions', on_delete=models.CASCADE)
    to_stage = models.ForeignKey(Stage, related_name='to_transitions', on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=User.ROLE_CHOICES)

    class Meta:
        unique_together = ('workflow', 'from_stage', 'to_stage', 'role')

    def __str__(self):
        return f"Transition in {self.workflow.name} from {self.from_stage.name} to {self.to_stage.name} by {self.role}"
