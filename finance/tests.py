from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import FeeStructure, FeePayment, Expense
from students.models import Student, Department
from auth_app.models import User
import datetime

class FinanceTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword',
            role='Admin'
        )
        self.client.force_authenticate(user=self.user)
        self.department = Department.objects.create(
            name='Computer Science',
            code='CS'
        )
        self.student = Student.objects.create(
            name='Test Student',
            roll_no='12345',
            department=self.department,
            semester=1
        )
        self.fee_structure = FeeStructure.objects.create(
            department=self.department,
            semester=1,
            tuition_fee=1000.00,
            examination_fee=100.00,
            other_fees=50.00
        )
        self.fee_payment = FeePayment.objects.create(
            student=self.student,
            fee_structure=self.fee_structure,
            amount_paid=1150.00,
            payment_date=datetime.date.today(),
            status='paid'
        )
        self.expense = Expense.objects.create(
            description='Test Expense',
            amount=500.00,
            date=datetime.date.today()
        )

    def test_create_fee_structure(self):
        url = reverse('feestructure-list')
        data = {
            'department': self.department.id,
            'semester': 2,
            'tuition_fee': 1200.00,
            'examination_fee': 120.00,
            'other_fees': 60.00
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(FeeStructure.objects.count(), 2)

    def test_get_fee_structures(self):
        url = reverse('feestructure-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_fee_payment(self):
        url = reverse('feepayment-list')
        data = {
            'student': self.student.id,
            'fee_structure': self.fee_structure.id,
            'amount_paid': 1150.00,
            'payment_date': datetime.date.today(),
            'status': 'paid'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(FeePayment.objects.count(), 2)

    def test_get_fee_payments(self):
        url = reverse('feepayment-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_expense(self):
        url = reverse('expense-list')
        data = {
            'description': 'New Expense',
            'amount': 600.00,
            'date': datetime.date.today()
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Expense.objects.count(), 2)

    def test_get_expenses(self):
        url = reverse('expense-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
