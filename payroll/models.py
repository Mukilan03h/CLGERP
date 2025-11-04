from django.db import models
from faculty.models import Faculty

class Salary(models.Model):
    """
    Defines the salary structure for a faculty member.
    """
    faculty = models.OneToOneField(Faculty, on_delete=models.CASCADE, related_name='salary')
    base_salary = models.DecimalField(max_digits=10, decimal_places=2, help_text="Monthly base salary")
    allowances = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="Monthly allowances")

    @property
    def gross_salary(self):
        return self.base_salary + self.allowances

    def __str__(self):
        return f"Salary for {self.faculty.name}"

class Payslip(models.Model):
    """
    Represents a monthly payslip for a faculty member.
    """
    PAYSLIP_STATUS = [
        ('Generated', 'Generated'),
        ('Paid', 'Paid'),
        ('Cancelled', 'Cancelled'),
    ]

    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='payslips')
    month = models.PositiveIntegerField()
    year = models.PositiveIntegerField()
    gross_salary = models.DecimalField(max_digits=12, decimal_places=2)
    total_deductions = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    net_salary = models.DecimalField(max_digits=12, decimal_places=2)
    generated_on = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=PAYSLIP_STATUS, default='Generated')

    class Meta:
        unique_together = ('faculty', 'month', 'year')

    def __str__(self):
        return f"Payslip for {self.faculty.name} - {self.month}/{self.year}"

class PayslipEntry(models.Model):
    """
    Represents a single line item in a payslip, either an earning or a deduction.
    """
    ENTRY_TYPES = [
        ('Earning', 'Earning'),
        ('Deduction', 'Deduction'),
    ]

    payslip = models.ForeignKey(Payslip, on_delete=models.CASCADE, related_name='entries')
    entry_type = models.CharField(max_length=10, choices=ENTRY_TYPES)
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name} ({self.entry_type}): {self.amount}"
