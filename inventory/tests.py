from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import InventoryItem, Asset
from auth_app.models import User
from students.models import Department
from faculty.models import Faculty

class InventoryModelTest(TestCase):
    def setUp(self):
        self.item = InventoryItem.objects.create(name='Test Item', category='Test Category', quantity=10)

    def test_inventory_item_creation(self):
        self.assertEqual(self.item.name, 'Test Item')
        self.assertEqual(self.item.quantity, 10)

class InventoryAPITest(APITestCase):
    def setUp(self):
        # Create users
        self.admin_user = User.objects.create_user(username='admin', password='password', role='Admin')
        self.student_user = User.objects.create_user(username='student', password='password', role='Student')

        # Create department and faculty
        self.department = Department.objects.create(name='Computer Science')
        self.faculty = Faculty.objects.create(name='Dr. Smith', department=self.department)

        # Create inventory item and asset
        self.item = InventoryItem.objects.create(name='Laptop', category='Electronics', quantity=5)
        self.asset = Asset.objects.create(
            item=self.item,
            asset_id='LAP123',
            purchase_date='2024-01-01',
            assigned_to_faculty=self.faculty
        )

        # URLs
        self.items_url = reverse('inventoryitem-list')
        self.item_detail_url = reverse('inventoryitem-detail', kwargs={'pk': self.item.pk})
        self.assets_url = reverse('asset-list')
        self.asset_detail_url = reverse('asset-detail', kwargs={'pk': self.asset.pk})

    def test_admin_can_create_item(self):
        self.client.force_authenticate(user=self.admin_user)
        data = {'name': 'New Item', 'category': 'New Category', 'quantity': 20}
        response = self.client.post(self.items_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_student_cannot_create_item(self):
        self.client.force_authenticate(user=self.student_user)
        data = {'name': 'Unauthorized Item', 'category': 'Category', 'quantity': 5}
        response = self.client.post(self.items_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_update_asset(self):
        self.client.force_authenticate(user=self.admin_user)
        data = {'location': 'New Location'}
        response = self.client.patch(self.asset_detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.asset.refresh_from_db()
        self.assertEqual(self.asset.location, 'New Location')

    def test_student_cannot_update_asset(self):
        self.client.force_authenticate(user=self.student_user)
        data = {'location': 'Unauthorized Location'}
        response = self.client.patch(self.asset_detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_any_authenticated_user_can_view_items(self):
        self.client.force_authenticate(user=self.student_user)
        response = self.client.get(self.items_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
