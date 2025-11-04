from django.db import models
from students.models import Student
from attendance.models import Subject

class Exam(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField()
    subjects = models.ManyToManyField(Subject)

    def __str__(self):
        return self.name

class Marks(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    marks = models.IntegerField()

    def __str__(self):
        return f'{self.student.name} - {self.subject.name} - {self.exam.name}'

class Result(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    total_marks = models.IntegerField()
    percentage = models.FloatField()
    grade = models.CharField(max_length=10)

    def __str__(self):
        return f'{self.student.name} - {self.exam.name}'
