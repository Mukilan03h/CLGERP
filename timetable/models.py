from django.db import models
from students.models import Department
from faculty.models import Faculty
from attendance.models import Subject

class Classroom(models.Model):
    room_no = models.CharField(max_length=10)
    capacity = models.IntegerField()

    def __str__(self):
        return self.room_no

class TimeSlot(models.Model):
    DAY_CHOICES = (
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
    )
    day = models.CharField(max_length=10, choices=DAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f'{self.day} - {self.start_time} to {self.end_time}'

class Timetable(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    semester = models.IntegerField()
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    timeslot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.department.name} - Semester {self.semester} - {self.subject.name}'
