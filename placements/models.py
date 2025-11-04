from django.db import models
from students.models import Student

class Company(models.Model):
    """
    Represents a company that recruits from the college.
    """
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    website = models.URLField(blank=True)

    def __str__(self):
        return self.name

class Job(models.Model):
    """
    Represents a job or internship opportunity.
    """
    JOB_TYPES = [
        ('Full-time', 'Full-time'),
        ('Part-time', 'Part-time'),
        ('Internship', 'Internship'),
    ]

    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='jobs')
    title = models.CharField(max_length=200)
    description = models.TextField()
    job_type = models.CharField(max_length=20, choices=JOB_TYPES)
    location = models.CharField(max_length=200, blank=True)
    posted_on = models.DateField(auto_now_add=True)
    application_deadline = models.DateField()

    def __str__(self):
        return f"{self.title} at {self.company.name}"

class Application(models.Model):
    """
    Represents a student's application for a job.
    """
    APPLICATION_STATUS = [
        ('Applied', 'Applied'),
        ('Shortlisted', 'Shortlisted'),
        ('Interviewing', 'Interviewing'),
        ('Offered', 'Offered'),
        ('Rejected', 'Rejected'),
        ('Accepted', 'Accepted'),
    ]

    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='applications')
    applied_on = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=APPLICATION_STATUS, default='Applied')
    resume = models.FileField(upload_to='resumes/')

    class Meta:
        unique_together = ('job', 'student')

    def __str__(self):
        return f"Application by {self.student.name} for {self.job.title}"
