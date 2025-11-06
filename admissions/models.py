from django.db import models
from students.models import Student
from workflow.models import Workflow, Stage

class Application(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    date_of_birth = models.DateField()
    address = models.TextField()
    previous_education = models.TextField()
    application_date = models.DateTimeField(auto_now_add=True)

    # Workflow integration
    workflow = models.ForeignKey(Workflow, on_delete=models.SET_NULL, null=True, blank=True, related_name='applications')
    current_stage = models.ForeignKey(Stage, on_delete=models.SET_NULL, null=True, blank=True, related_name='applications')

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class Admission(models.Model):
    application = models.OneToOneField(Application, on_delete=models.CASCADE)
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    admission_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Admission for {self.student}'
