from django.db import models
from auth_app.models import User

class Department(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    roll_no = models.CharField(max_length=20, unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    semester = models.IntegerField()
    guardian_info = models.TextField()
    documents = models.FileField(upload_to='documents/', blank=True, null=True)

    def __str__(self):
        return self.name
