from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Classroom, TimeSlot, Timetable
from students.models import Student, Department
from faculty.models import Faculty
from attendance.models import Subject
from auth_app.models import User

class TimetablePermissionsTests(APITestCase):

    def setUp(self):
        self.admin_user = User.objects.create_user(username='admin', password='password', role='Admin')
        self.faculty_user = User.objects.create_user(username='faculty', password='password', role='Faculty')
        self.student_user = User.objects.create_user(username='student', password='password', role='Student')

        self.department = Department.objects.create(name='Computer Science', code='CS')
        self.other_department = Department.objects.create(name='Electrical Engineering', code='EE')

        self.student = Student.objects.create(user=self.student_user, name='Test Student', roll_no='123', department=self.department, semester=1, guardian_info='Test Guardian')
        self.faculty = Faculty.objects.create(user=self.faculty_user, name='Test Faculty', department=self.department, designation='Professor')

        self.subject = Subject.objects.create(name='Data Structures', code='CS101', department=self.department, semester=1)
        self.classroom = Classroom.objects.create(room_no='101', capacity=50)
        self.timeslot = TimeSlot.objects.create(day='Monday', start_time='09:00:00', end_time='10:00:00')

        self.timetable = Timetable.objects.create(department=self.department, semester=1, subject=self.subject, faculty=self.faculty, classroom=self.classroom, timeslot=self.timeslot)

    def test_admin_can_list_all_timetables(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(reverse('timetable-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_student_can_view_own_timetable(self):
        self.client.force_authenticate(user=self.student_user)
        response = self.client.get(reverse('timetable-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_student_cannot_view_other_timetable(self):
        other_timetable = Timetable.objects.create(department=self.other_department, semester=1, subject=self.subject, faculty=self.faculty, classroom=self.classroom, timeslot=self.timeslot)
        self.client.force_authenticate(user=self.student_user)
        response = self.client.get(reverse('timetable-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_faculty_can_view_own_department_timetable(self):
        self.client.force_authenticate(user=self.faculty_user)
        response = self.client.get(reverse('timetable-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_admin_can_create_timetable(self):
        self.client.force_authenticate(user=self.admin_user)
        data = {'department': self.department.id, 'semester': 1, 'subject': self.subject.id, 'faculty': self.faculty.id, 'classroom': self.classroom.id, 'timeslot': self.timeslot.id}
        response = self.client.post(reverse('timetable-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_faculty_cannot_create_timetable(self):
        self.client.force_authenticate(user=self.faculty_user)
        data = {'department': self.department.id, 'semester': 1, 'subject': self.subject.id, 'faculty': self.faculty.id, 'classroom': self.classroom.id, 'timeslot': self.timeslot.id}
        response = self.client.post(reverse('timetable-list'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
