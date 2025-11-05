from django.db import models
from students.models import Student, Department

class FeeStructure(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    semester = models.IntegerField()
    tuition_fee = models.DecimalField(max_digits=10, decimal_places=2)
    examination_fee = models.DecimalField(max_digits=10, decimal_places=2)
    other_fees = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.department.name} - Semester {self.semester}'

class FeePayment(models.Model):
    PAYMENT_STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('waived', 'Waived'),
    )

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    fee_structure = models.ForeignKey(FeeStructure, on_delete=models.CASCADE)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField()
    status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default='pending')

    def __str__(self):
        return f'{self.student} - {self.fee_structure}'

class Expense(models.Model):
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()

    def __str__(self):
        return self.description
