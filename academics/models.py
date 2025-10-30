from django.db import models

class Program(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    duration = models.IntegerField()

    def __str__(self):
        return self.name

class Course(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    credits = models.IntegerField()
    semester = models.IntegerField()

    def __str__(self):
        return self.name

class Syllabus(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return f'Syllabus for {self.course.name}'
