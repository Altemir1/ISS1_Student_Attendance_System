from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from attendance.models import attendance, specific_course, course, card_of_student, students_courses
from attendance.views import att_toggle
from account.models import  Teacher, Student
from datetime import time
from django.utils import timezone
from datetime import datetime, timedelta

class AttendanceViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.student = Student.objects.create_user(
            id='testid', password='testpassword', email='testemail@sdu.kz'
        )
        self.teacher = Teacher.objects.create_user(
            id='testteach', password='testpassword'
        )
        self.course = course.objects.create(
            course_code='CS101',
            credits='3',
            hours=45,
            course_name='Introduction to Computer Science',
            ECTS=5
        )
        self.specific_course = specific_course.objects.create(
            course_code='CS101',
            is_lecture=True,
            specific_course_id=1,
            course_part=1,
            course_start_time=time(8, 30, 0),
            course_start_day=1
        )
        self.attendance = attendance.objects.create(
            student_id='testid',
            specific_course_id=1,
            status=2,
            weak_count = 1,
            att_id = 1,
        )
        self.client.post(reverse('account:login'), {'id': 'testteach', 'password': 'testpassword', 'role':'teacher'})

    def test_att_toggle(self):
        response = self.client.get(reverse('attendance:att_toggle', args=('1', 'CS101', '1', 'L')))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(attendance.objects.get(att_id='1').status, 1)
        
class CardReaderViewTest(TestCase):
    def setUp(self):
        # Setup mock data for card_of_student, specific_course, students_courses, and attendance
        student = card_of_student.objects.create(uid='1234567', student_id='student01')
        course = specific_course.objects.create(course_code='ABCD123', specific_course_id=1, group=1, course_part=1, course_start_time=timezone.now().time())
        students_courses.objects.create(student_id=student.student_id, specific_course_id=course.specific_course_id)
        attendance.objects.create(student_id=student.student_id, specific_course_id=course.specific_course_id, date=timezone.now().date(), status=0)

    def test_no_uid_provided(self):
        response = self.client.get(reverse('attendance:card_reader'))
        self.assertEqual(response.status_code, 400)
        self.assertIn('No UID provided', response.content.decode())

    def test_valid_uid(self):
        response = self.client.get(reverse('attendance:card_reader'), {'uid': '12345670'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('It worked', response.content.decode())
        
        attendance_record = attendance.objects.first()
        self.assertEqual(attendance_record.status, 0)

    def test_invalid_uid(self):
        response = self.client.get(reverse('attendance:card_reader'), {'uid': 'invalid00'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('It worked', response.content.decode())
        # Check that no changes were made to the attendance
        attendance_record = attendance.objects.first()
        self.assertEqual(attendance_record.status, 0)

