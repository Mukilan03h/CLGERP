from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Exam(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField()
    subjects = models.ManyToManyField('attendance.Subject')

    def __str__(self):
        return self.name

class Marks(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE)
    subject = models.ForeignKey('attendance.Subject', on_delete=models.CASCADE)
    marks = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])

    def __str__(self):
        return f'{self.student} - {self.subject} - {self.marks}'

class Result(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE)
    total_marks = models.IntegerField()
    percentage = models.FloatField()
    grade = models.CharField(max_length=10)

    def __str__(self):
        return f'{self.student} - {self.exam}'
