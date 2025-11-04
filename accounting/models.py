from django.db import models
from auth_app.models import User

class Ledger(models.Model):
    """
    Represents a financial account in the accounting system.
    """
    ACCOUNT_TYPES = [
        ('Asset', 'Asset'),
        ('Liability', 'Liability'),
        ('Equity', 'Equity'),
        ('Revenue', 'Revenue'),
        ('Expense', 'Expense'),
    ]

    name = models.CharField(max_length=100, unique=True)
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPES)
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.name} ({self.account_type})"

class Transaction(models.Model):
    """
    Represents a financial transaction between two ledgers (double-entry).
    """
    TRANSACTION_TYPES = [
        ('Debit', 'Debit'),
        ('Credit', 'Credit'),
    ]

    date = models.DateField()
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    debit_account = models.ForeignKey(Ledger, on_delete=models.PROTECT, related_name='debits')
    credit_account = models.ForeignKey(Ledger, on_delete=models.PROTECT, related_name='credits')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transaction of {self.amount} on {self.date}"

    def save(self, *args, **kwargs):
        # This is a simplified implementation. A real-world scenario would need to handle this atomically.
        self.debit_account.balance += self.amount
        self.credit_account.balance -= self.amount
        self.debit_account.save()
        self.credit_account.save()
        super().save(*args, **kwargs)
