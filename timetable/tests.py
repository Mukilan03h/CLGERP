from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Classroom, TimeSlot, Timetable
from students.models import Student, Department
from faculty.models import Faculty
from attendance.models import Subject
from auth_app.models import User

class TimetableModelTest(APITestCase):
    def setUp(self):
        self.department = Department.objects.create(name='Computer Science', code='CS')
        self.faculty = Faculty.objects.create(name='Dr. Smith', department=self.department, designation='Professor')
        self.subject = Subject.objects.create(name='Data Structures', code='CS101', semester=1)
        self.classroom = Classroom.objects.create(room_no='101', capacity=50)
        self.timeslot = TimeSlot.objects.create(day='Monday', start_time='09:00:00', end_time='10:00:00')

    def test_timetable_creation(self):
        timetable = Timetable.objects.create(
            department=self.department,
            semester=1,
            subject=self.subject,
            faculty=self.faculty,
            classroom=self.classroom,
            timeslot=self.timeslot
        )
        self.assertEqual(Timetable.objects.count(), 1)
        self.assertEqual(timetable.subject.name, 'Data Structures')

class TimetableAPITest(APITestCase):
    def setUp(self):
        self.department = Department.objects.create(name='Computer Science', code='CS')
        self.student_user = User.objects.create_user(username='student', password='password', role='Student')
        self.student = Student.objects.create(user=self.student_user, name='John Doe', roll_no='123', department=self.department, semester=1)
        self.faculty_user = User.objects.create_user(username='faculty', password='password', role='Faculty')
        self.faculty = Faculty.objects.create(user=self.faculty_user, name='Dr. Smith', department=self.department, designation='Professor')
        self.subject = Subject.objects.create(name='Data Structures', code='CS101', semester=1)
        self.classroom = Classroom.objects.create(room_no='101', capacity=50)
        self.timeslot = TimeSlot.objects.create(day='Monday', start_time='09:00:00', end_time='10:00:00')
        self.timetable = Timetable.objects.create(
            department=self.department,
            semester=1,
            subject=self.subject,
            faculty=self.faculty,
            classroom=self.classroom,
            timeslot=self.timeslot
        )

    def test_student_can_view_own_timetable(self):
        self.client.force_authenticate(user=self.student_user)
        url = reverse('timetable-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_student_cannot_view_other_timetable(self):
        other_department = Department.objects.create(name='Mechanical', code='ME')
        other_timetable = Timetable.objects.create(
            department=other_department,
            semester=1,
            subject=self.subject,
            faculty=self.faculty,
            classroom=self.classroom,
            timeslot=self.timeslot
        )
        self.client.force_authenticate(user=self.student_user)
        url = reverse('timetable-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertNotContains(response, other_timetable.id)

    def test_faculty_can_view_own_timetable(self):
        self.client.force_authenticate(user=self.faculty_user)
        url = reverse('timetable-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_faculty_cannot_create_timetable_for_other_faculty(self):
        other_faculty_user = User.objects.create_user(username='other_faculty', password='password', role='Faculty')
        other_faculty = Faculty.objects.create(user=other_faculty_user, name='Dr. Jones', department=self.department, designation='Professor')
        self.client.force_authenticate(user=self.faculty_user)
        url = reverse('timetable-list')
        data = {
            'department': self.department.id,
            'semester': 1,
            'subject': self.subject.id,
            'faculty': other_faculty.id,
            'classroom': self.classroom.id,
            'timeslot': self.timeslot.id
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
