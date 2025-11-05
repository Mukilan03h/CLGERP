from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Salary, Payslip, PayslipEntry
from auth_app.models import User
from students.models import Department
from faculty.models import Faculty

class PayrollAPITest(APITestCase):
    def setUp(self):
        # Users
        self.admin_user = User.objects.create_user(username='admin', password='password', role='Admin')
        self.faculty_user = User.objects.create_user(username='faculty', password='password', role='Faculty')
        self.other_faculty_user = User.objects.create_user(username='other_faculty', password='password', role='Faculty')

        # Department and Faculty
        self.department = Department.objects.create(name='Chemistry')
        self.faculty = Faculty.objects.create(name='Dr. Green', department=self.department, user=self.faculty_user, designation='Professor')
        self.other_faculty = Faculty.objects.create(name='Dr. White', department=self.department, user=self.other_faculty_user, designation='Professor')

        # Salary and Payslip
        self.salary = Salary.objects.create(faculty=self.faculty, base_salary=60000, allowances=7000)
        self.payslip = Payslip.objects.create(
            faculty=self.faculty,
            month=1,
            year=2024,
            gross_salary=67000,
            total_deductions=5000,
            net_salary=62000
        )
        self.payslip_entry = PayslipEntry.objects.create(payslip=self.payslip, entry_type='Earning', name='House Rent Allowance', amount=5000)


    def test_admin_can_create_salary(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('salary-list')
        data = {'faculty': self.other_faculty.pk, 'base_salary': 55000, 'allowances': 6000}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_faculty_cannot_create_salary(self):
        self.client.force_authenticate(user=self.faculty_user)
        url = reverse('salary-list')
        data = {'faculty': self.other_faculty.pk, 'base_salary': 55000, 'allowances': 6000}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_faculty_can_view_own_payslip(self):
        self.client.force_authenticate(user=self.faculty_user)
        url = reverse('payslip-detail', kwargs={'pk': self.payslip.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_faculty_cannot_view_others_payslip(self):
        self.client.force_authenticate(user=self.other_faculty_user)
        url = reverse('payslip-detail', kwargs={'pk': self.payslip.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_admin_can_view_any_payslip(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('payslip-detail', kwargs={'pk': self.payslip.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_faculty_can_view_own_payslip_entry(self):
        self.client.force_authenticate(user=self.faculty_user)
        url = reverse('payslipentry-detail', kwargs={'pk': self.payslip_entry.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
