from django.db import models
from students.models import Student, Department

class ApplicationForm(models.Model):
    student_info = models.ForeignKey(Student, on_delete=models.CASCADE)
    score = models.FloatField()
    status = models.CharField(max_length=20, default='Pending')
    documents = models.FileField(upload_to='admission_documents/', blank=True, null=True)

    def __str__(self):
        return f'{self.student_info.name} - {self.status}'

class MeritList(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    rank = models.IntegerField()
    student_ref = models.ForeignKey(Student, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.department.name} - Rank {self.rank}'
