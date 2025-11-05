from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Notification
from auth_app.models import User

class NotificationAPITest(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='password')
        self.user2 = User.objects.create_user(username='user2', password='password')
        self.notification1 = Notification.objects.create(recipient=self.user1, message='Notification 1')
        self.notification2 = Notification.objects.create(recipient=self.user2, message='Notification 2')

    def test_user_can_list_own_notifications(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse('notification-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['message'], 'Notification 1')

    def test_user_cannot_list_others_notifications(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse('notification-detail', kwargs={'pk': self.notification2.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_can_mark_own_notification_as_read(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse('notification-mark-as-read', kwargs={'pk': self.notification1.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.notification1.refresh_from_db()
        self.assertTrue(self.notification1.is_read)

    def test_user_can_mark_all_own_notifications_as_read(self):
        Notification.objects.create(recipient=self.user1, message='Another one')
        self.client.force_authenticate(user=self.user1)
        url = reverse('notification-mark-all-as-read')
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for notification in self.user1.notifications.all():
            self.assertTrue(notification.is_read)
