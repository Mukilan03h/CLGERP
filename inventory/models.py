from django.db import models
from faculty.models import Faculty
from students.models import Department

class InventoryItem(models.Model):
    """
    Represents a type of item in the inventory, e.g., 'Dell Latitude Laptop'.
    """
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

class Asset(models.Model):
    """
    Represents a specific, trackable asset, which is an instance of an InventoryItem.
    """
    ASSET_CONDITIONS = [
        ('New', 'New'),
        ('Good', 'Good'),
        ('Used', 'Used'),
        ('Damaged', 'Damaged'),
        ('Retired', 'Retired'),
    ]

    item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE, related_name='assets')
    asset_id = models.CharField(max_length=100, unique=True, help_text="Unique identifier for the asset (e.g., serial number, tag)")
    purchase_date = models.DateField()
    condition = models.CharField(max_length=50, choices=ASSET_CONDITIONS, default='New')
    location = models.CharField(max_length=200, blank=True)

    # An asset can be assigned to a specific faculty member or a department
    assigned_to_faculty = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True, blank=True)
    assigned_to_department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'{self.item.name} ({self.asset_id})'
