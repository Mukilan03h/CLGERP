from django.db import models
from students.models import Student

class Vehicle(models.Model):
    vehicle_no = models.CharField(max_length=20, unique=True)
    vehicle_type = models.CharField(max_length=50)
    capacity = models.PositiveIntegerField()

    def __str__(self):
        return self.vehicle_no

class Route(models.Model):
    name = models.CharField(max_length=100)
    stops = models.TextField()

    def __str__(self):
        return self.name

class TransportAllocation(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    date_allocated = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.student.name} - {self.route.name}'
