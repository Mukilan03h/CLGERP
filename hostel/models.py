from django.db import models
from students.models import Student

class Hostel(models.Model):
    name = models.CharField(max_length=100)
    capacity = models.IntegerField()

    def __str__(self):
        return self.name

class Room(models.Model):
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE)
    room_no = models.CharField(max_length=10)
    capacity = models.IntegerField()
    is_vacant = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.hostel.name} - Room {self.room_no}'

class Allocation(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date_allocated = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.student.name} - {self.room}'
