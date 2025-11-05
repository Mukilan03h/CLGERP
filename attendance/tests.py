from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Subject, Attendance
from students.models import Student, Department
from auth_app.models import User
from faculty.models import Faculty
import datetime

class AttendancePermissionsTests(APITestCase):

    def setUp(self):
        self.admin_user = User.objects.create_user(username='admin', password='password', role='Admin')
        self.faculty_user = User.objects.create_user(username='faculty', password='password', role='Faculty')
        self.student_user = User.objects.create_user(username='student', password='password', role='Student')
        self.other_student_user = User.objects.create_user(username='other_student', password='password', role='Student')

        self.department = Department.objects.create(name='Computer Science', code='CS')
        self.other_department = Department.objects.create(name='Electrical Engineering', code='EE')

        self.student = Student.objects.create(user=self.student_user, name='Test Student', roll_no='123', department=self.department, semester=1, guardian_info='Test Guardian')
        self.other_student = Student.objects.create(user=self.other_student_user, name='Other Student', roll_no='456', department=self.other_department, semester=1, guardian_info='Other Guardian')

        self.faculty = Faculty.objects.create(user=self.faculty_user, name='Test Faculty', department=self.department, designation='Professor')

        self.subject = Subject.objects.create(name='Data Structures', code='CS101', department=self.department, semester=1)
        self.faculty.subjects.add(self.subject)

        self.attendance = Attendance.objects.create(student=self.student, subject=self.subject, date=datetime.date.today(), status='present')

    def test_admin_can_list_all_subjects(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(reverse('subject-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_student_can_list_subjects_in_their_department(self):
        self.client.force_authenticate(user=self.student_user)
        response = self.client.get(reverse('subject-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_student_can_view_own_attendance(self):
        self.client.force_authenticate(user=self.student_user)
        response = self.client.get(reverse('attendance-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_student_cannot_view_other_attendance(self):
        self.client.force_authenticate(user=self.other_student_user)
        response = self.client.get(reverse('attendance-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_faculty_can_create_attendance_for_own_subject(self):
        self.client.force_authenticate(user=self.faculty_user)
        data = {'student': self.student.id, 'subject': self.subject.id, 'date': datetime.date.today(), 'status': 'absent'}
        response = self.client.post(reverse('attendance-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_faculty_cannot_create_attendance_for_other_subject(self):
        other_subject = Subject.objects.create(name='Algorithms', code='CS102', department=self.department, semester=1)
        self.client.force_authenticate(user=self.faculty_user)
        data = {'student': self.student.id, 'subject': other_subject.id, 'date': datetime.date.today(), 'status': 'absent'}
        response = self.client.post(reverse('attendance-list'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_attendance_with_invalid_status(self):
        self.client.force_authenticate(user=self.faculty_user)
        data = {'student': self.student.id, 'subject': self.subject.id, 'date': datetime.date.today(), 'status': 'invalid'}
        response = self.client.post(reverse('attendance-list'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_student_cannot_update_attendance(self):
        self.client.force_authenticate(user=self.student_user)
        data = {'status': 'absent'}
        response = self.client.patch(reverse('attendance-detail', kwargs={'pk': self.attendance.pk}), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
