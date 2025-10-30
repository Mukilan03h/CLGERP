from django.db import models
from students.models import Department

class Faculty(models.Model):
    name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    designation = models.CharField(max_length=100)
    subjects = models.ManyToManyField('attendance.Subject')

    def __str__(self):
        return self.name

class LeaveRequest(models.Model):
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=20, default='Pending')

    def __str__(self):
        return f'{self.faculty.name} - {self.start_date} to {self.end_date}'
