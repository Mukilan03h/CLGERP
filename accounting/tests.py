from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Ledger, Transaction
from auth_app.models import User
import datetime

class AccountingModelTest(TestCase):
    def setUp(self):
        self.asset_ledger = Ledger.objects.create(name='Cash', account_type='Asset', balance=1000)
        self.expense_ledger = Ledger.objects.create(name='Office Supplies', account_type='Expense')

    def test_transaction_updates_balance(self):
        Transaction.objects.create(
            date=datetime.date.today(),
            description='Bought pens',
            amount=50,
            debit_account=self.expense_ledger,
            credit_account=self.asset_ledger
        )
        self.asset_ledger.refresh_from_db()
        self.expense_ledger.refresh_from_db()
        self.assertEqual(self.asset_ledger.balance, 950)
        self.assertEqual(self.expense_ledger.balance, 50)

class AccountingAPITest(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_user(username='admin', password='password', role='Admin')
        self.accountant_user = User.objects.create_user(username='accountant', password='password', role='Accountant')
        self.student_user = User.objects.create_user(username='student', password='password', role='Student')

        self.ledger1 = Ledger.objects.create(name='Accounts Receivable', account_type='Asset')
        self.ledger2 = Ledger.objects.create(name='Sales Revenue', account_type='Revenue')

        self.ledgers_url = reverse('ledger-list')
        self.transactions_url = reverse('transaction-list')

    def test_admin_can_create_ledger(self):
        self.client.force_authenticate(user=self.admin_user)
        data = {'name': 'Office Equipment', 'account_type': 'Asset'}
        response = self.client.post(self.ledgers_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_accountant_can_create_transaction(self):
        self.client.force_authenticate(user=self.accountant_user)
        data = {
            'date': datetime.date.today(),
            'description': 'Invoice #123',
            'amount': 500,
            'debit_account': self.ledger1.pk,
            'credit_account': self.ledger2.pk
        }
        response = self.client.post(self.transactions_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_student_cannot_access_ledgers(self):
        self.client.force_authenticate(user=self.student_user)
        response = self.client.get(self.ledgers_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_student_cannot_create_transaction(self):
        self.client.force_authenticate(user=self.student_user)
        data = {
            'date': datetime.date.today(),
            'description': 'Unauthorized transaction',
            'amount': 100,
            'debit_account': self.ledger1.pk,
            'credit_account': self.ledger2.pk
        }
        response = self.client.post(self.transactions_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
